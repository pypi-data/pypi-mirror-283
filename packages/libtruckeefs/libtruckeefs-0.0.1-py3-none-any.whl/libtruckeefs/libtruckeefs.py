import struct
import errno
import array
import heapq
import zlib
import itertools
import os
import time
import json
import threading
import codecs
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import hmac
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from urllib.request import Request
from urllib.request import urlopen
from urllib.parse import quote
from urllib.error import HTTPError
import shutil
import logging
import sys
import fcntl
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.hazmat.primitives.ciphers import modes
from cryptography.hazmat.backends import default_backend

######## START CONTENT ########


BLOCK_SIZE = 131072
BLOCK_UNALLOCATED = -1
BLOCK_ZERO = -2


def ceildiv(a, b):
	"""Compute ceil(a/b); i.e. rounded towards positive infinity"""
	return 1 + (a-1)//b


class BlockStorage(object):
	"""
	File storing fixed-size blocks of data.
	"""

	def __init__(this, f, block_size):
		this.f = f
		this.block_size = block_size
		this.block_map = array.array('l')
		this.zero_block = b"\x00"*this.block_size
		this._reconstruct_free_map()

	def save_state(this, f):
		f.truncate(0)
		f.seek(0)
		f.write(b"BLK2")

		# Using zlib here is mainly for obfuscating information on the
		# total size of sparse files. The size of the map file will
		# correlate with the amount of downloaded data, but
		# compression reduces its correlation with the total size of
		# the file.
		block_map_data = zlib.compress(this.block_map.tobytes(), 9)
		f.write(struct.pack('<QQ', this.block_size, len(block_map_data)))
		f.write(block_map_data)

	@classmethod
	def restore_state(cls, f, state_file):
		hdr = state_file.read(4)
		if hdr != b"BLK2":
			raise ValueError("invalid block storage state file")
		s = state_file.read(2 * 8)
		block_size, data_size = struct.unpack('<QQ', s)

		try:
			s = zlib.decompress(state_file.read(data_size))
		except zlib.error:
			raise ValueError("invalid block map data")
		block_map = array.array('l')
		block_map.frombytes(s)
		del s

		this = cls.__new__(cls)
		this.f = f
		this.block_size = block_size
		this.block_map = block_map
		this.zero_block = b"\x00"*this.block_size
		this._reconstruct_free_map()
		return this

	def _reconstruct_free_map(this):
		if this.block_map:
			max_block = max(this.block_map)
		else:
			max_block = -1

		if max_block < 0:
			this.free_block_idx = 0
			this.free_map = []
			return

		mask = array.array('b', itertools.repeat(0, max_block+1))
		for x in this.block_map:
			if x >= 0:
				mask[x] = 1

		free_map = [j for j, x in enumerate(mask) if x == 0]
		heapq.heapify(free_map)

		this.free_map = free_map
		this.free_block_idx = max_block + 1

	def _get_free_block_idx(this):
		if this.free_map:
			return heapq.heappop(this.free_map)
		idx = this.free_block_idx
		this.free_block_idx += 1
		return idx

	def _add_free_block_idx(this, idx):
		heapq.heappush(this.free_map, idx)

	def _truncate_free_map(this, end_block):
		this.free_block_idx = end_block
		last_map_size = len(this.free_map)
		this.free_map = [x for x in this.free_map if x < end_block]
		if last_map_size != len(this.free_map):
			heapq.heapify(this.free_map)

	def __contains__(this, idx):
		if not idx >= 0:
			raise ValueError("Invalid block index")
		if idx >= len(this.block_map):
			return False
		return this.block_map[idx] != BLOCK_UNALLOCATED

	def __getitem__(this, idx):
		if idx not in this:
			raise KeyError("Block %d not allocated" % (idx,))

		block_idx = this.block_map[idx]
		if block_idx >= 0:
			this.f.seek(this.block_size * block_idx)
			block = this.f.read(this.block_size)
			if len(block) < this.block_size:
				# Partial block (end-of-file): consider zero-padded
				block += b"\x00"*(this.block_size - len(block))
			return block
		elif block_idx == BLOCK_ZERO:
			return this.zero_block
		else:
			raise IOError(errno.EIO, "Corrupted block map data")

	def __setitem__(this, idx, data):
		if not idx >= 0:
			raise ValueError("Invalid block index")
		if idx >= len(this.block_map):
			this.block_map.extend(itertools.repeat(BLOCK_UNALLOCATED, idx + 1 - len(this.block_map)))

		if data is None or data == this.zero_block:
			block_idx = this.block_map[idx]
			if block_idx >= 0:
				this._add_free_block_idx(block_idx)
			this.block_map[idx] = BLOCK_ZERO
		else:
			if len(data) > this.block_size:
				raise ValueError("Too large data block")

			block_idx = this.block_map[idx]
			if not block_idx >= 0:
				block_idx = this._get_free_block_idx()

			this.block_map[idx] = block_idx

			if len(data) < this.block_size:
				# Partial blocks are OK at the end of the file
				# only. Such blocks will be automatically zero-padded
				# by POSIX if writes are done to subsequent blocks.
				# Other blocks need explicit padding.
				this.f.seek(0, 2)
				pos = this.f.tell()
				if pos > this.block_size * block_idx + len(data):
					data += b"\x00" * (this.block_size - len(data))

			this.f.seek(this.block_size * block_idx)
			this.f.write(data)

	def truncate(this, num_blocks):
		this.block_map = this.block_map[:num_blocks]

		end_block = 0
		if this.block_map:
			end_block = max(0, max(this.block_map) + 1)
		this.f.truncate(this.block_size * end_block)
		this._truncate_free_map(end_block)


class BlockCachedFile(object):
	"""
	I am temporary file, caching data for a remote file. I support
	overwriting data. I cache remote data on a per-block basis and
	keep track of which blocks need still to be retrieved. Before each
	read/write operation, my pre_read or pre_write method needs to be
	called --- these give the ranges of data that need to be retrieved
	from the remote file and fed to me (via receive_cached_data)
	before the read/write operation can succeed. I am fully
	synchronous.
	"""

	def __init__(this, f, initial_cache_size, block_size=None):
		if block_size is None:
			block_size = BLOCK_SIZE
		this.size = initial_cache_size
		this.storage = BlockStorage(f, block_size)
		this.block_size = this.storage.block_size
		this.first_uncached_block = 0
		this.cache_size = initial_cache_size

	def save_state(this, f):
		this.storage.save_state(f)
		f.write(struct.pack('<QQQ', this.size, this.cache_size, this.first_uncached_block))

	@classmethod
	def restore_state(cls, f, state_file):
		storage = BlockStorage.restore_state(f, state_file)
		s = state_file.read(3 * 8)
		size, cache_size, first_uncached_block = struct.unpack('<QQQ', s)

		this = cls.__new__(cls)
		this.storage = storage
		this.size = size
		this.cache_size = cache_size
		this.first_uncached_block = first_uncached_block
		this.block_size = this.storage.block_size
		return this

	def _pad_file(this, new_size):
		"""
		Append zero bytes that the virtual size grows to new_size
		"""
		if new_size <= this.size:
			return

		# Fill remainder blocks in the file with nulls; the last
		# existing block, if partial, is implicitly null-padded
		start, mid, end = block_range(this.size, new_size - this.size, block_size=this.block_size)

		if start is not None and start[1] == 0:
			this.storage[start[0]] = None

		if mid is not None:
			for idx in range(*mid):
				this.storage[idx] = None

		if end is not None:
			this.storage[end[0]] = None

		this.size = new_size

	def receive_cached_data(this, offset, data_list):
		"""
		Write full data blocks to file, unless they were not written
		yet. Returns (new_offset, new_data_list) containing unused,
		possibly reuseable data. data_list is a list of strings.
		"""
		data_size = sum(len(data) for data in data_list)

		start, mid, end = block_range(offset, data_size, last_pos=this.cache_size,
									  block_size=this.block_size)

		if mid is None:
			# not enough data for full blocks
			return offset, data_list

		data = b"".join(data_list)

		i = 0
		if start is not None:
			# skip initial part
			i = this.block_size - start[1]

		for j in range(*mid):
			if j not in this.storage:
				block = data[i:i+this.block_size]
				this.storage[j] = block
			i += min(this.block_size, data_size - i)

		if mid[0] <= this.first_uncached_block:
			this.first_uncached_block = max(this.first_uncached_block, mid[1])

		# Return trailing data for possible future use
		if i < data_size:
			data_list = [data[i:]]
		else:
			data_list = []
		offset += i
		return (offset, data_list)

	def get_size(this):
		return this.size

	def get_file(this):
		# Pad file to full size before returning file handle
		this._pad_file(this.get_size())
		return BlockCachedFileHandle(this)

	def close(this):
		this.storage.f.close()
		this.storage = None

	def truncate(this, size):
		if size < this.size:
			this.storage.truncate(ceildiv(size, this.block_size))
			this.size = size
		elif size > this.size:
			this._pad_file(size)

		this.cache_size = min(this.cache_size, size)

	def write(this, offset, data):
		if offset > this.size:
			# Explicit POSIX behavior for write-past-end
			this._pad_file(offset)

		if len(data) == 0:
			# noop
			return

		# Perform write
		start, mid, end = block_range(offset, len(data), block_size=this.block_size)

		# Pad virtual size
		this._pad_file(offset + len(data))

		# Write first block
		if start is not None:
			block = this.storage[start[0]]
			i = start[2] - start[1]
			this.storage[start[0]] = block[:start[1]] + data[:i] + block[start[2]:]
		else:
			i = 0

		# Write intermediate blocks
		if mid is not None:
			for idx in range(*mid):
				this.storage[idx] = data[i:i+this.block_size]
				i += this.block_size

		# Write last block
		if end is not None:
			block = this.storage[end[0]]
			this.storage[end[0]] = data[i:] + block[end[1]:]

	def read(this, offset, length):
		length = max(0, min(this.size - offset, length))
		if length == 0:
			return b''

		# Perform read
		start, mid, end = block_range(offset, length, block_size=this.block_size)

		datas = []

		# Read first block
		if start is not None:
			datas.append(this.storage[start[0]][start[1]:start[2]])

		# Read intermediate blocks
		if mid is not None:
			for idx in range(*mid):
				datas.append(this.storage[idx])

		# Read last block
		if end is not None:
			datas.append(this.storage[end[0]][:end[1]])

		return b"".join(datas)

	def pre_read(this, offset, length):
		"""
		Return (offset, length) of the first cache fetch that need to be
		performed and the results fed into `receive_cached_data` before a read
		operation can be performed. There may be more than one fetch
		necessary. Return None if no fetch is necessary.
		"""

		# Limit to inside the cached area
		cache_end = ceildiv(this.cache_size, this.block_size) * this.block_size
		length = max(0, min(length, cache_end - offset))
		if length == 0:
			return None

		# Find bounds of the read operation
		start_block = offset//this.block_size
		end_block = ceildiv(offset + length, this.block_size)

		# Combine consequent blocks into a single read
		j = max(start_block, this.first_uncached_block)
		while j < end_block and j in this.storage:
			j += 1
		if j >= end_block:
			return None

		for k in range(j+1, end_block):
			if k in this.storage:
				end = k
				break
		else:
			end = end_block

		if j >= end:
			return None

		start_pos = j * this.block_size
		end_pos = end * this.block_size
		if start_pos < this.cache_size:
			return (start_pos, min(end_pos, this.cache_size) - start_pos)

		return None

	def pre_write(this, offset, length):
		"""
		Similarly to pre_read, but for write operations.
		"""
		start, mid, end = block_range(offset, length, block_size=this.block_size)

		# Writes only need partially available blocks to be in the cache
		for item in (start, end):
			if item is not None and item[0] >= this.first_uncached_block and item[0] not in this.storage:
				start_pos = item[0] * this.block_size
				end_pos = (item[0] + 1) * this.block_size
				if start_pos < this.cache_size:
					return (start_pos, min(this.cache_size, end_pos) - start_pos)

		# No reads required
		return None


class BlockCachedFileHandle(object):
	"""
	Read-only access to BlockCachedFile, as if it was a contiguous file
	"""
	def __init__(this, block_cached_file):
		this.block_cached_file = block_cached_file
		this.pos = 0

	def seek(this, offset, whence=0):
		if whence == 0:
			this.pos = offset
		elif whence == 1:
			this.pos += offset
		elif whence == 2:
			this.pos = offset + this.block_cached_file.get_size()
		else:
			raise ValueError("Invalid whence")

	def read(this, size=None):
		if size is None:
			size = max(0, this.block_cached_file.get_size() - this.pos)
		data = this.block_cached_file.read(this.pos, size)
		this.pos += len(data)
		return data


def block_range(offset, length, block_size, last_pos=None):
	"""
	Get the blocks that overlap with data range [offset, offset+length]

	Parameters
	----------
	offset, length : int
		Range specification
	last_pos : int, optional
		End-of-file position. If the data range goes over the end of the file,
		the last block is the last block in `mid`, and `end` is None.

	Returns
	-------
	start : (idx, start_pos, end_pos) or None
		Partial block at the beginning; block[start_pos:end_pos] has the data. If missing: None
	mid : (start_idx, end_idx)
		Range [start_idx, end_idx) of full blocks in the middle. If missing: None
	end : (idx, end_pos)
		Partial block at the end; block[:end_pos] has the data. If missing: None

	"""
	if last_pos is not None:
		length = max(min(last_pos - offset, length), 0)

	if length == 0:
		return None, None, None

	start_block, start_pos = divmod(offset, block_size)
	end_block, end_pos = divmod(offset + length, block_size)

	if last_pos is not None:
		if offset + length == last_pos and end_pos > 0:
			end_block += 1
			end_pos = 0

	if start_block == end_block:
		if start_pos == end_pos:
			return None, None, None
		return (start_block, start_pos, end_pos), None, None

	mid = None

	if start_pos == 0:
		start = None
		mid = (start_block, end_block)
	else:
		start = (start_block, start_pos, block_size)
		if start_block+1 < end_block:
			mid = (start_block+1, end_block)

	if end_pos == 0:
		end = None
	else:
		end = (end_block, end_pos)

	return start, mid, end

"""
Cache metadata and data of a directory tree for read-only access.
"""





class TahoeResponse(object):
	def __init__(this, connection, req, is_put, timeout):
		this.connection = connection

		# XXX: We use default timeout for PUT requests, for now:
		#	  Solution would be to limit send buffer size, but urllib2
		#	  doesn't easily allow this Switching to requests module probably
		#	  would help.
		#
		# We recv data in relatively small blocks, so that blocking
		# for recv corresponds roughly to network activity. POST
		# requests are also small, so that the situation is the same.
		#
		# However, PUT requests may upload large amounts of data. The
		# send buffer can also be fairly large, so that all the data
		# may fit into it. In this case, we end up blocking on reading
		# the server response, which arrives only after the data in
		# the buffer is sent. In this case, timeout can arrive even if
		# the computer is still successfully uploading data ---
		# blocking does not correspond to network activity.
		#
		if is_put:
			this.response = urlopen(req)
		else:
			this.response = urlopen(req, timeout=timeout)
		this.is_put = is_put

	def read(this, size=None):
		return this.response.read(size)

	def close(this):
		this.response.close()
		this.connection._release_response(this, this.is_put)


class TahoeConnection(object):
	def __init__(this, base_url, rootcap, timeout, max_connections=10):
		assert isinstance(base_url, str)
		assert isinstance(rootcap, str)

		this.base_url = base_url.rstrip('/') + '/uri'
		this.rootcap = rootcap.encode('utf-8')

		this.connections = []
		this.lock = threading.Lock()

		put_conns = max(1, max_connections//2)
		get_conns = max(1, max_connections - put_conns)

		this.get_semaphore = threading.Semaphore(get_conns)
		this.put_semaphore = threading.Semaphore(put_conns)
		this.timeout = timeout

	def _get_response(this, req, is_put):
		semaphore = this.put_semaphore if is_put else this.get_semaphore

		semaphore.acquire()
		try:
			response = TahoeResponse(this, req, is_put, this.timeout)
			with this.lock:
				this.connections.append(response)
				return response
		except:
			semaphore.release()
			raise

	def _release_response(this, response, is_put):
		semaphore = this.put_semaphore if is_put else this.get_semaphore

		with this.lock:
			if response in this.connections:
				semaphore.release()
				this.connections.remove(response)

	def wait_until_write_allowed(this):
		# Force wait if put queue is full
		this.put_semaphore.acquire()
		this.put_semaphore.release()

	def _url(this, path, params={}, iscap=False):
		assert isinstance(path, str), path

		path = quote(path).lstrip('/')
		if iscap:
			path = this.base_url + '/' + path
		else:
			path = this.base_url + '/' + this.rootcap.decode('ascii') + '/' + path

		if params:
			path += '?'

			for k, v in list(params.items()):
				assert isinstance(k, str), k
				assert isinstance(v, str), v
				if not path.endswith('?'):
					path += '&'
				k = quote(k, safe='')
				v = quote(v, safe='')
				path += k
				path += '='
				path += v

		return path

	def _get_request(this, method, path, offset=None, length=None, data=None, params={}, iscap=False):
		headers = {'Accept': 'text/plain'}

		if offset is not None or length is not None:
			if offset is None:
				start = "0"
				offset = 0
			else:
				start = str(offset)
			if length is None:
				end = ""
			else:
				end = str(offset + length - 1)
			headers['Range'] = 'bytes=' + start + '-' + end

		req = Request(this._url(path, params, iscap=iscap),
					  data=data,
					  headers=headers)
		req.get_method = lambda: method
		return req

	def _get(this, path, params={}, offset=None, length=None, iscap=False):
		req = this._get_request("GET", path, params=params, offset=offset, length=length, iscap=iscap)
		return this._get_response(req, False)

	def _post(this, path, data=None, params={}, iscap=False):
		req = this._get_request("POST", path, data=data, params=params, iscap=iscap)
		return this._get_response(req, False)

	def _put(this, path, data=None, params={}, iscap=False):
		req = this._get_request("PUT", path, data=data, params=params, iscap=iscap)
		return this._get_response(req, True)

	def _delete(this, path, params={}, iscap=False):
		req = this._get_request("DELETE", path, params=params, iscap=iscap)
		return this._get_response(req, False)

	def get_info(this, path, iscap=False):
		f = this._get(path, {'t': 'json'}, iscap=iscap)
		try:
			data = json.load(f)
		finally:
			f.close()
		return data

	def get_content(this, path, offset=None, length=None, iscap=False):
		return this._get(path, offset=offset, length=length, iscap=iscap)

	def put_file(this, path, f, iscap=False):
		f = this._put(path, data=f, iscap=iscap)
		try:
			return f.read().decode('utf-8').strip()
		finally:
			f.close()

	def delete(this, path, iscap=False):
		f = this._delete(path, iscap=iscap)
		try:
			return f.read().decode('utf-8').strip()
		finally:
			f.close()

	def mkdir(this, path, iscap=False):
		f = this._post(path, params={'t': 'mkdir'}, iscap=iscap)
		try:
			return f.read().decode('utf-8').strip()
		finally:
			f.close()

"""
Cache metadata and data of a directory tree.
"""



backend = default_backend()

BLOCK_SIZE = 131072


class CryptFile(object):
	"""
	File encrypted with a key in AES-CBC mode, in BLOCK_SIZE blocks,
	with random IV for each block.
	"""

	IV_SIZE = 16
	HEADER_SIZE = IV_SIZE + 16

	def __init__(this, path, key, mode='r+b', block_size=BLOCK_SIZE):
		this.key = None
		this.path = path

		if len(key) != 32:
			raise ValueError("Key must be 32 bytes")

		if mode == 'rb':
			fd = os.open(path, os.O_RDONLY)
		elif mode == 'r+b':
			fd = os.open(path, os.O_RDWR)
		elif mode == 'w+b':
			fd = os.open(path, os.O_RDWR | os.O_CREAT, 0o0600)
		else:
			raise IOError(errno.EACCES, "Unsupported mode %r" % (mode,))

		try:
			# BSD locking on the file; only one fd can write at a time
			if mode == 'rb':
				fcntl.flock(fd, fcntl.LOCK_SH)
			else:
				fcntl.flock(fd, fcntl.LOCK_EX)

			if mode == 'w+b':
				# Truncate after locking
				os.ftruncate(fd, 0)

			this.fp = os.fdopen(fd, mode)
		except:
			os.close(fd)
			raise

		this.mode = mode
		this.key = key

		assert algorithms.AES.block_size//8 == 16

		if block_size % 16 != 0:
			raise ValueError("Block size must be multiple of AES block size")
		this.block_size = block_size

		if mode == 'w+b':
			this.data_size = 0
		else:
			# Read header
			try:
				iv = this.fp.read(this.IV_SIZE)
				if len(iv) != this.IV_SIZE:
					raise ValueError()

				cipher = Cipher(algorithms.AES(this.key), modes.CBC(iv), backend=backend)
				decryptor = cipher.decryptor()

				ciphertext = this.fp.read(16)
				if len(ciphertext) != 16:
					raise ValueError()
				data = decryptor.update(ciphertext) + decryptor.finalize()
				this.data_size = struct.unpack('<Q', data[8:])[0]

				# Check the data size is OK
				this.fp.seek(0, 2)
				file_size = this.fp.tell()
				num_blocks, remainder = divmod(file_size - this.HEADER_SIZE, this.IV_SIZE + block_size)
				if remainder > 0:
					num_blocks += 1
				if this.data_size == 0 and num_blocks == 1:
					# Zero-size files can contain 0 or 1 data blocks
					num_blocks = 0
				if not ((num_blocks-1)*block_size < this.data_size <= num_blocks*block_size):
					raise ValueError()
			except (IOError, struct.error, ValueError):
				this.fp.close()
				raise ValueError("invalid header data in file")

		this.current_block = -1
		this.block_cache = b""
		this.block_dirty = False

		this.offset = 0

	def _write_header(this):
		iv = os.urandom(this.IV_SIZE)
		cipher = Cipher(algorithms.AES(this.key), modes.CBC(iv), backend=backend)
		encryptor = cipher.encryptor()

		this.fp.seek(0)
		this.fp.write(iv)

		data = os.urandom(8) + struct.pack("<Q", this.data_size)
		this.fp.write(encryptor.update(data))
		this.fp.write(encryptor.finalize())

	def _flush_block(this):
		if this.current_block < 0:
			return
		if not this.block_dirty:
			return

		iv = os.urandom(this.IV_SIZE)
		cipher = Cipher(algorithms.AES(this.key), modes.CBC(iv), backend=backend)
		encryptor = cipher.encryptor()

		this.fp.seek(this.HEADER_SIZE + this.current_block * (this.IV_SIZE + this.block_size))
		this.fp.write(iv)

		off = (len(this.block_cache) % 16)
		if off == 0:
			this.fp.write(encryptor.update(bytes(this.block_cache)))
		else:
			# insert random padding
			this.fp.write(encryptor.update(bytes(this.block_cache) + os.urandom(16-off)))
		this.fp.write(encryptor.finalize())

		this.block_dirty = False

	def _load_block(this, i):
		if i == this.current_block:
			return

		this._flush_block()

		this.fp.seek(this.HEADER_SIZE + i * (this.IV_SIZE + this.block_size))
		iv = this.fp.read(this.IV_SIZE)

		if not iv:
			# Block does not exist, past end of file
			this.current_block = i
			this.block_cache = b""
			this.block_dirty = False
			return

		ciphertext = this.fp.read(this.block_size)
		cipher = Cipher(algorithms.AES(this.key), modes.CBC(iv), backend=backend)
		decryptor = cipher.decryptor()

		if (i+1)*this.block_size > this.data_size:
			size = this.data_size - i*this.block_size
		else:
			size = this.block_size

		this.current_block = i
		this.block_cache = (decryptor.update(ciphertext) + decryptor.finalize())[:size]
		this.block_dirty = False

	def seek(this, offset, whence=0):
		if whence == 0:
			pass
		elif whence == 1:
			offset = this.offset + offset
		elif whence == 2:
			offset += this.data_size
		else:
			raise IOError(errno.EINVAL, "Invalid whence")
		if offset < 0:
			raise IOError(errno.EINVAL, "Invalid offset")
		this.offset = offset

	def tell(this):
		return this.offset

	def _get_file_size(this):
		this.fp.seek(0, 2)
		return this.fp.tell()

	def _read(this, size, offset):
		if size is None:
			size = this.data_size - offset
		if size <= 0:
			return b""

		start_block, start_off = divmod(offset, this.block_size)
		end_block, end_off = divmod(offset + size, this.block_size)
		if end_off != 0:
			end_block += 1

		# Read and decrypt data
		data = []
		for i in range(start_block, end_block):
			this._load_block(i)
			data.append(this.block_cache)

		if end_off != 0:
			data[-1] = data[-1][:end_off]
		data[0] = data[0][start_off:]
		return b"".join(map(bytes, data))

	def _write(this, data, offset):
		size = len(data)
		start_block, start_off = divmod(offset, this.block_size)
		end_block, end_off = divmod(offset + size, this.block_size)

		k = 0

		if this.mode == 'rb':
			raise IOError(errno.EACCES, "Write to a read-only file")

		# Write first block, if partial
		if start_off != 0 or end_block == start_block:
			this._load_block(start_block)
			data_block = data[:(this.block_size - start_off)]
			this.block_cache = this.block_cache[:start_off] + data_block + this.block_cache[start_off+len(data_block):]
			this.block_dirty = True
			k += 1
			start_block += 1

		# Write full blocks
		for i in range(start_block, end_block):
			if this.current_block != i:
				this._flush_block()
			this.current_block = i
			this.block_cache = data[k*this.block_size-start_off:(k+1)*this.block_size-start_off]
			this.block_dirty = True
			k += 1

		# Write last partial block
		if end_block > start_block and end_off != 0:
			this._load_block(end_block)
			data_block = data[k*this.block_size-start_off:(k+1)*this.block_size-start_off]
			this.block_cache = data_block + this.block_cache[len(data_block):]
			this.block_dirty = True

		this.data_size = max(this.data_size, offset + len(data))

	def read(this, size=None):
		data = this._read(size, this.offset)
		this.offset += len(data)
		return data

	def write(this, data):
		if this.data_size < this.offset:
			# Write past end
			s = NullString(this.offset - this.data_size)
			this._write(s, this.data_size)

		this._write(data, this.offset)
		this.offset += len(data)

	def truncate(this, size):
		last_block, last_off = divmod(size, this.block_size)

		this._load_block(last_block)
		last_block_data = this.block_cache

		# truncate to block boundary
		this._flush_block()
		sz = this.HEADER_SIZE + last_block * (this.IV_SIZE + this.block_size)
		this.fp.truncate(sz)
		this.data_size = last_block * this.block_size
		this.current_block = -1
		this.block_cache = b""
		this.block_dirty = False

		# rewrite the last block
		if last_off != 0:
			this._write(last_block_data[:last_off], this.data_size)

		# add null padding
		if this.data_size < size:
			s = NullString(size - this.data_size)
			this._write(s, this.data_size)

	def __enter__(this):
		return this

	def __exit__(this, exc_type, exc_value, traceback):
		this.close()
		return False

	def flush(this):
		if this.mode != 'rb':
			this._flush_block()
			this._write_header()
		this.fp.flush()

	def close(this):
		if this.key is None:
			return
		if this.mode != 'rb':
			this.flush()
		this.fp.close()
		this.key = None

	def __del__(this):
		this.close()


class NullString(object):
	def __init__(this, size):
		this.size = size

	def __len__(this):
		return this.size

	def __getitem__(this, k):
		if isinstance(k, slice):
			return b"\x00" * len(range(*k.indices(this.size)))
		else:
			raise IndexError("invalid index")



class CacheDB(object):
	def __init__(this, path, rootcap, node_url, cache_size, cache_data,
				 read_lifetime, write_lifetime):
		path = os.path.abspath(path)
		if not os.path.isdir(path):
			raise IOError(errno.ENOENT, "Cache directory is not an existing directory")

		assert isinstance(rootcap, str)

		this.cache_size = cache_size
		this.cache_data = cache_data
		this.read_lifetime = read_lifetime
		this.write_lifetime = write_lifetime

		this.path = path
		this.key, this.salt_hkdf = this._generate_prk(rootcap)

		this.last_size_check_time = 0

		# Cache lock
		this.lock = threading.RLock()

		# Open files and dirs
		this.open_items = {}

		# Restrict cache size
		this._restrict_size()

		# Directory cache
		this._max_item_cache = 500
		this._item_cache = []

	def _generate_prk(this, rootcap):
		# Cache master key is derived from hashed rootcap and salt via
		# PBKDF2, with a fixed number of iterations.
		#
		# The master key, combined with a second different salt, are
		# used to generate per-file keys via HKDF-SHA256

		# Get salt
		salt_fn = os.path.join(this.path, 'salt')
		try:
			with open(salt_fn, 'rb') as f:
				numiter = f.read(4)
				salt = f.read(32)
				salt_hkdf = f.read(32)
				if len(numiter) != 4 or len(salt) != 32 or len(salt_hkdf) != 32:
					raise ValueError()
				numiter = struct.unpack('<I', numiter)[0]
		except (IOError, OSError, ValueError):
			# Start with new salt
			rnd = os.urandom(64)
			salt = rnd[:32]
			salt_hkdf = rnd[32:]

			# Determine suitable number of iterations
			start = time.time()
			count = 0
			while True:
				kdf = PBKDF2HMAC(
					algorithm=hashes.SHA256(),
					length=32,
					salt=b"b"*len(salt),
					iterations=10000,
					backend=backend
				)
				kdf.derive(b"a"*len(rootcap.encode('ascii')))
				count += 10000
				if time.time() > start + 0.05:
					break
			numiter = max(10000, int(count * 1.0 / (time.time() - start)))

			# Write salt etc.
			with open(salt_fn, 'wb') as f:
				f.write(struct.pack('<I', numiter))
				f.write(salt)
				f.write(salt_hkdf)

		# Derive key
		kdf = PBKDF2HMAC(
			algorithm=hashes.SHA256(),
			length=32,
			salt=salt,
			iterations=numiter,
			backend=backend
		)
		key = kdf.derive(rootcap.encode('ascii'))

		# HKDF private key material for per-file keys
		return key, salt_hkdf

	def _walk_cache_subtree(this, root_upath=""):
		"""
		Walk through items in the cached directory tree, starting from
		the given root point.

		Yields
		------
		filename, upath
			Filename and corresponding upath of a reached cached entry.

		"""
		stack = []

		# Start from root
		fn, key = this.get_filename_and_key(root_upath)
		if os.path.isfile(fn):
			stack.append((root_upath, fn, key))

		# Walk the tree
		while stack:
			upath, fn, key = stack.pop()

			if not os.path.isfile(fn):
				continue

			try:
				with CryptFile(fn, key=key, mode='rb') as f:
					data = json_zlib_load(f)
					if data[0] == 'dirnode':
						children = list(data[1].get('children', {}).items())
					else:
						children = []
			except (IOError, OSError, ValueError):
				continue

			yield (os.path.basename(fn), upath)

			for c_fn, c_info in children:
				c_upath = os.path.join(upath, c_fn)
				if c_info[0] == 'dirnode':
					c_fn, c_key = this.get_filename_and_key(c_upath)
					if os.path.isfile(c_fn):
						stack.append((c_upath, c_fn, c_key))
				elif c_info[0] == 'filenode':
					for ext in (None, b'state', b'data'):
						c_fn, c_key = this.get_filename_and_key(c_upath, ext=ext)
						yield (os.path.basename(c_fn), c_upath)

	def _restrict_size(this):
		def get_cache_score(entry):
			fn, st = entry
			return -cache_score(size=st.st_size, t=now-st.st_mtime)

		with this.lock:
			now = time.time()
			if now < this.last_size_check_time + 60:
				return

			this.last_size_check_time = now

			files = [os.path.join(this.path, fn) 
					 for fn in os.listdir(this.path) 
					 if fn != "salt"]
			entries = [(fn, os.stat(fn)) for fn in files]
			entries.sort(key=get_cache_score)

			tot_size = 0
			for fn, st in entries:
				if tot_size + st.st_size > this.cache_size:
					# unlink
					os.unlink(fn)
				else:
					tot_size += st.st_size

	def _invalidate(this, root_upath="", shallow=False):
		if root_upath == "" and not shallow:
			for f in this.open_items.values():
				f.invalidated = True
			this.open_items = {}
			dead_file_set = os.listdir(this.path)
		else:
			dead_file_set = set()
			for fn, upath in this._walk_cache_subtree(root_upath):
				f = this.open_items.pop(upath, None)
				if f is not None:
					f.invalidated = True
				dead_file_set.add(fn)
				if shallow and upath != root_upath:
					break

		for basename in dead_file_set:
			if basename == 'salt':
				continue
			fn = os.path.join(this.path, basename)
			if os.path.isfile(fn):
				os.unlink(fn)

	def invalidate(this, root_upath="", shallow=False):
		with this.lock:
			this._invalidate(root_upath, shallow=shallow)

	def open_file(this, upath, io, flags, lifetime=None):
		with this.lock:
			writeable = (flags & (os.O_RDONLY | os.O_RDWR | os.O_WRONLY)) in (os.O_RDWR, os.O_WRONLY)
			if writeable:
				# Drop file data cache before opening in write mode
				if upath not in this.open_items:
					this.invalidate(upath)

				# Limit e.g. parent directory lookup lifetime
				if lifetime is None:
					lifetime = this.write_lifetime

			f = this.get_file_inode(upath, io,
									excl=(flags & os.O_EXCL),
									creat=(flags & os.O_CREAT),
									lifetime=lifetime)
			return CachedFileHandle(upath, f, flags)

	def open_dir(this, upath, io, lifetime=None):
		with this.lock:
			f = this.get_dir_inode(upath, io, lifetime=lifetime)
			return CachedDirHandle(upath, f)

	def close_file(this, f):
		with this.lock:
			c = f.inode
			upath = f.upath
			f.close()
			if c.closed:
				if upath in this.open_items:
					del this.open_items[upath]
				this._restrict_size()

	def close_dir(this, f):
		with this.lock:
			c = f.inode
			upath = f.upath
			f.close()
			if c.closed:
				if upath in this.open_items:
					del this.open_items[upath]
				this._restrict_size()

	def upload_file(this, c, io):
		if isinstance(c, CachedFileHandle):
			c = c.inode

		if c.upath is not None and c.dirty:
			parent = this.open_dir(udirname(c.upath), io, lifetime=this.write_lifetime)
			try:
				parent_cap = parent.inode.info[1]['rw_uri']

				# Upload
				try:
					cap = c.upload(io, parent_cap=parent_cap)
				except:
					# Failure to upload --- need to invalidate parent
					# directory, since the file might not have been
					# created.
					this.invalidate(parent.upath, shallow=True)
					raise

				# Add in cache
				with this.lock:
					parent.inode.cache_add_child(ubasename(c.upath), cap, size=c.get_size())
			finally:
				this.close_dir(parent)

	def unlink(this, upath, io, is_dir=False):
		if upath == '':
			raise IOError(errno.EACCES, "cannot unlink root directory")

		with this.lock:
			# Unlink in cache
			if is_dir:
				f = this.open_dir(upath, io, lifetime=this.write_lifetime)
			else:
				f = this.open_file(upath, io, 0, lifetime=this.write_lifetime)
			try:
				f.inode.unlink()
			finally:
				if is_dir:
					this.close_dir(f)
				else:
					this.close_file(f)

			# Perform unlink
			parent = this.open_dir(udirname(upath), io, lifetime=this.write_lifetime)
			try:
				parent_cap = parent.inode.info[1]['rw_uri']

				upath_cap = parent_cap + '/' + ubasename(upath)
				try:
					cap = io.delete(upath_cap, iscap=True)
				except (HTTPError, IOError) as err:
					if isinstance(err, HTTPError) and err.code == 404:
						raise IOError(errno.ENOENT, "no such file")
					raise IOError(errno.EREMOTEIO, "failed to retrieve information")

				# Remove from cache
				parent.inode.cache_remove_child(ubasename(upath))
			finally:
				this.close_dir(parent)

	def mkdir(this, upath, io):
		if upath == '':
			raise IOError(errno.EEXIST, "cannot re-mkdir root directory")

		with this.lock:
			# Check that parent exists
			parent = this.open_dir(udirname(upath), io, lifetime=this.write_lifetime)
			try:
				parent_cap = parent.inode.info[1]['rw_uri']

				# Check that the target does not exist
				try:
					parent.get_child_attr(ubasename(upath))
				except IOError as err:
					if err.errno == errno.ENOENT:
						pass
					else:
						raise
				else:
					raise IOError(errno.EEXIST, "directory already exists")

				# Invalidate cache
				this.invalidate(upath)

				# Perform operation
				upath_cap = parent_cap + '/' + ubasename(upath)
				try:
					cap = io.mkdir(upath_cap, iscap=True)
				except (HTTPError, IOError) as err:
					raise IOError(errno.EREMOTEIO, "remote operation failed: {0}".format(err))

				# Add in cache
				parent.inode.cache_add_child(ubasename(upath), cap, size=None)
			finally:
				this.close_dir(parent)

	def get_attr(this, upath, io):
		if upath == '':
			dir = this.open_dir(upath, io)
			try:
				info = dir.get_attr()
			finally:
				this.close_dir(dir)
		else:
			upath_parent = udirname(upath)
			dir = this.open_dir(upath_parent, io)
			try:
				info = dir.get_child_attr(ubasename(upath))
			except IOError as err:
				with this.lock:
					if err.errno == errno.ENOENT and upath in this.open_items:
						# New file that has not yet been uploaded
						info = dict(this.open_items[upath].get_attr())
						if 'mtime' not in info:
							info['mtime'] = time.time()
						if 'ctime' not in info:
							info['ctime'] = time.time()
					else:
						raise
			finally:
				this.close_dir(dir)

		with this.lock:
			if upath in this.open_items:
				info.update(this.open_items[upath].get_attr())
				if 'mtime' not in info:
					info['mtime'] = time.time()
				if 'ctime' not in info:
					info['ctime'] = time.time()

		return info

	def _lookup_cap(this, upath, io, read_only=True, lifetime=None):
		if lifetime is None:
			lifetime = this.read_lifetime

		with this.lock:
			if upath in this.open_items and this.open_items[upath].is_fresh(lifetime):
				# shortcut
				if read_only:
					return this.open_items[upath].info[1]['ro_uri']
				else:
					return this.open_items[upath].info[1]['rw_uri']
			elif upath == '':
				# root
				return None
			else:
				# lookup from parent
				entry_name = ubasename(upath)
				parent_upath = udirname(upath)

				parent = this.open_dir(parent_upath, io, lifetime=lifetime)
				try:
					if read_only:
						return parent.get_child_attr(entry_name)['ro_uri']
					else:
						return parent.get_child_attr(entry_name)['rw_uri']
				finally:
					this.close_dir(parent)

	def get_file_inode(this, upath, io, excl=False, creat=False, lifetime=None):
		if lifetime is None:
			lifetime = this.read_lifetime

		with this.lock:
			f = this.open_items.get(upath)

			if f is not None and not f.is_fresh(lifetime):
				f = None
				this.invalidate(upath, shallow=True)

			if f is None:
				try:
					cap = this._lookup_cap(upath, io, lifetime=lifetime)
				except IOError as err:
					if err.errno == errno.ENOENT and creat:
						cap = None
					else:
						raise

				if excl and cap is not None:
					raise IOError(errno.EEXIST, "file already exists")
				if not creat and cap is None:
					raise IOError(errno.ENOENT, "file does not exist")

				f = CachedFileInode(this, upath, io, filecap=cap, 
									persistent=this.cache_data)
				this.open_items[upath] = f

				if cap is None:
					# new file: add to parent inode
					d = this.open_dir(udirname(upath), io, lifetime=lifetime)
					try:
						d.inode.cache_add_child(ubasename(upath), None, size=0)
					finally:
						this.close_dir(d)
				return f
			else:
				if excl:
					raise IOError(errno.EEXIST, "file already exists")
				if not isinstance(f, CachedFileInode):
					raise IOError(errno.EISDIR, "item is a directory")
				return f

	def get_dir_inode(this, upath, io, lifetime=None):
		if lifetime is None:
			lifetime = this.read_lifetime

		with this.lock:
			f = this.open_items.get(upath)

			if f is not None and not f.is_fresh(lifetime):
				f = None
				this.invalidate(upath, shallow=True)

			if f is None:
				cap = this._lookup_cap(upath, io, read_only=False, lifetime=lifetime)
				f = CachedDirInode(this, upath, io, dircap=cap)
				this.open_items[upath] = f

				# Add to item cache
				cache_item = (time.time(), CachedDirHandle(upath, f))
				if len(this._item_cache) < this._max_item_cache:
					heapq.heappush(this._item_cache, cache_item)
				else:
					old_time, old_fh = heapq.heapreplace(this._item_cache,
														 cache_item)
					this.close_dir(old_fh)

				return f
			else:
				if not isinstance(f, CachedDirInode):
					raise IOError(errno.ENOTDIR, "item is a file")
				return f

	def get_upath_parent(this, path):
		return this.get_upath(os.path.dirname(os.path.normpath(path)))

	def get_upath(this, path):
		assert isinstance(path, str)
		try:
			path = os.path.normpath(path)
			return path.replace(os.sep, "/").lstrip('/')
		except UnicodeError:
			raise IOError(errno.ENOENT, "file does not exist")

	def path_from_upath(this, upath):
		return upath.replace(os.sep, "/")

	def get_filename_and_key(this, upath, ext=None):
		path = upath.encode('utf-8')
		nonpath = b"//\x00" # cannot occur in path, which is normalized

		# Generate per-file key material via HKDF
		info = path
		if ext is not None:
			info += nonpath + ext

		hkdf = HKDF(algorithm=hashes.SHA256(),
					length=3*32,
					salt=this.salt_hkdf,
					info=info,
					backend=backend)
		data = hkdf.derive(this.key)

		# Generate key
		key = data[:32]

		# Generate filename
		h = hmac.HMAC(key=data[32:], algorithm=hashes.SHA512(), backend=backend)
		h.update(info)
		fn = codecs.encode(h.finalize(), 'hex_codec').decode('ascii')
		return os.path.join(this.path, fn), key


class CachedFileHandle(object):
	"""
	Logical file handle. There may be multiple open file handles
	corresponding to the same logical file.
	"""

	direct_io = False
	keep_cache = False

	def __init__(this, upath, inode, flags):
		this.inode = inode
		this.inode.incref()
		this.lock = threading.RLock()
		this.flags = flags
		this.upath = upath

		this.writeable = (this.flags & (os.O_RDONLY | os.O_RDWR | os.O_WRONLY)) in (os.O_RDWR, os.O_WRONLY)
		this.readable = (this.flags & (os.O_RDONLY | os.O_RDWR | os.O_WRONLY)) in (os.O_RDWR, os.O_RDONLY)
		this.append = (this.flags & os.O_APPEND)

		if this.flags & os.O_ASYNC:
			raise IOError(errno.ENOTSUP, "O_ASYNC flag is not supported")
		if this.flags & os.O_DIRECT:
			raise IOError(errno.ENOTSUP, "O_DIRECT flag is not supported")
		if this.flags & os.O_DIRECTORY:
			raise IOError(errno.ENOTSUP, "O_DIRECTORY flag is not supported")
		if this.flags & os.O_SYNC:
			raise IOError(errno.ENOTSUP, "O_SYNC flag is not supported")
		if (this.flags & os.O_CREAT) and not this.writeable:
			raise IOError(errno.EINVAL, "O_CREAT without writeable file")
		if (this.flags & os.O_TRUNC) and not this.writeable:
			raise IOError(errno.EINVAL, "O_TRUNC without writeable file")
		if (this.flags & os.O_EXCL) and not this.writeable:
			raise IOError(errno.EINVAL, "O_EXCL without writeable file")
		if (this.flags & os.O_APPEND) and not this.writeable:
			raise IOError(errno.EINVAL, "O_EXCL without writeable file")

		if (this.flags & os.O_TRUNC):
			this.inode.truncate(0)

	def close(this):
		with this.lock:
			if this.inode is None:
				raise IOError(errno.EBADF, "Operation on a closed file")
			c = this.inode
			this.inode = None
			c.decref()

	def read(this, io, offset, length):
		with this.lock:
			if this.inode is None:
				raise IOError(errno.EBADF, "Operation on a closed file")
			if not this.readable:
				raise IOError(errno.EBADF, "File not readable")
			return this.inode.read(io, offset, length)

	def get_size(this):
		with this.lock:
			return this.inode.get_size()

	def write(this, io, offset, data):
		with this.lock:
			if this.inode is None:
				raise IOError(errno.EBADF, "Operation on a closed file")
			if not this.writeable:
				raise IOError(errno.EBADF, "File not writeable")
			if this.append:
				offset = None
			return this.inode.write(io, offset, data)

	def truncate(this, size):
		with this.lock:
			if this.inode is None:
				raise IOError(errno.EBADF, "Operation on a closed file")
			if not this.writeable:
				raise IOError(errno.EBADF, "File not writeable")
			return this.inode.truncate(size)


class CachedDirHandle(object):
	"""
	Logical directory handle.
	"""

	def __init__(this, upath, inode):
		this.inode = inode
		this.inode.incref()
		this.lock = threading.RLock()
		this.upath = upath

	def close(this):
		with this.lock:
			if this.inode is None:
				raise IOError(errno.EBADF, "Operation on a closed dir")
			c = this.inode
			this.inode = None
			c.decref()

	def listdir(this):
		with this.lock:
			if this.inode is None:
				raise IOError(errno.EBADF, "Operation on a closed dir")
			return this.inode.listdir()

	def get_attr(this):
		with this.lock:
			if this.inode is None:
				raise IOError(errno.EBADF, "Operation on a closed dir")
			return this.inode.get_attr()

	def get_child_attr(this, childname):
		with this.lock:
			if this.inode is None:
				raise IOError(errno.EBADF, "Operation on a closed dir")
			return this.inode.get_child_attr(childname)


class CachedFileInode(object):
	"""
	Logical file on-disk. There should be only a single CachedFileInode
	instance is per each logical file.
	"""

	def __init__(this, cachedb, upath, io, filecap, persistent=False):
		this.upath = upath
		this.closed = False
		this.refcnt = 0
		this.persistent = persistent
		this.invalidated = False

		# Use per-file keys for different files, for safer fallback
		# in the extremely unlikely event of SHA512 hash collisions
		filename, key = cachedb.get_filename_and_key(upath)
		filename_state, key_state = cachedb.get_filename_and_key(upath, b'state')
		filename_data, key_data = cachedb.get_filename_and_key(upath, b'data')

		this.lock = threading.RLock()
		this.cache_lock = threading.RLock()
		this.dirty = False
		this.f = None
		this.f_state = None
		this.f_data = None

		this.stream_f = None
		this.stream_offset = 0
		this.stream_data = []

		open_complete = False

		try:
			if filecap is None:
				# Create new file
				raise ValueError()

			# Reuse cached metadata
			this.f = CryptFile(filename, key=key, mode='r+b')
			this.info = json_zlib_load(this.f)

			if persistent:
				# Reuse cached data
				this.f_state = CryptFile(filename_state, key=key_state, mode='r+b')
				this.f_data = CryptFile(filename_data, key=key_data, mode='r+b')
				this.block_cache = BlockCachedFile.restore_state(this.f_data, this.f_state)
				open_complete = True
		except (IOError, OSError, ValueError):
			open_complete = False
			if this.f is not None:
				this.f.close()
				this.f = None
			if this.f_state is not None:
				this.f_state.close()
			if this.f_data is not None:
				this.f_data.close()

		if not open_complete:
			if this.f is None:
				this.f = CryptFile(filename, key=key, mode='w+b')
				try:
					if filecap is not None:
						this._load_info(filecap, io, iscap=True)
					else:
						this.info = ['file', {'size': 0}]
						this.dirty = True
				except IOError as err:
					os.unlink(filename)
					this.f.close()
					raise

			# Create a data file
			this.f_data = CryptFile(filename_data, key=key_data, mode='w+b')

			# Block cache on top of data file
			this.block_cache = BlockCachedFile(this.f_data, this.info[1]['size'])

			# Block data state file
			this.f_state = CryptFile(filename_state, key=key_state, mode='w+b')

		os.utime(this.f.path, None)
		os.utime(this.f_data.path, None)
		os.utime(this.f_state.path, None)

	def _load_info(this, upath, io, iscap=False):
		try:
			this.info = io.get_info(upath, iscap=iscap)
		except (HTTPError, IOError, ValueError) as err:
			if isinstance(err, HTTPError) and err.code == 404:
				raise IOError(errno.ENOENT, "no such file")
			raise IOError(errno.EREMOTEIO, "failed to retrieve information")
		this._save_info()

	def _save_info(this):
		this.f.truncate(0)
		this.f.seek(0)
		if 'retrieved' not in this.info[1]:
			this.info[1]['retrieved'] = time.time()
		json_zlib_dump(this.info, this.f)

	def is_fresh(this, lifetime):
		if 'retrieved' not in this.info[1]:
			return True
		return (this.info[1]['retrieved'] + lifetime >= time.time())

	def incref(this):
		with this.cache_lock:
			this.refcnt += 1

	def decref(this):
		with this.cache_lock:
			this.refcnt -= 1
			if this.refcnt <= 0:
				this.close()

	def close(this):
		with this.cache_lock, this.lock:
			if not this.closed:
				if this.stream_f is not None:
					this.stream_f.close()
					this.stream_f = None
					this.stream_data = []
				this.f_state.seek(0)
				this.f_state.truncate(0)
				this.block_cache.save_state(this.f_state)
				this.f_state.close()
				this.block_cache.close()
				this.f.close()

				if not this.persistent and this.upath is not None and not this.invalidated:
					os.unlink(this.f_state.path)
					os.unlink(this.f_data.path)
			this.closed = True

	def _do_rw(this, io, offset, length_or_data, write=False, no_result=False):
		if write:
			data = length_or_data
			length = len(data)
		else:
			length = length_or_data

		while True:
			with this.cache_lock:
				if write:
					pos = this.block_cache.pre_write(offset, length)
				else:
					pos = this.block_cache.pre_read(offset, length)

				if pos is None:
					# cache ready
					if no_result:
						return None
					elif write:
						return this.block_cache.write(offset, data)
					else:
						return this.block_cache.read(offset, length)

			# cache not ready -- fill it up
			with this.lock:
				try:
					c_offset, c_length = pos

					if this.stream_f is not None and (this.stream_offset > c_offset or
													  c_offset >= this.stream_offset + 3*131072):
						this.stream_f.close()
						this.stream_f = None
						this.stream_data = []

					if this.stream_f is None:
						this.stream_f = io.get_content(this.info[1]['ro_uri'], c_offset, iscap=True)
						this.stream_offset = c_offset
						this.stream_data = []

					read_offset = this.stream_offset
					read_bytes = sum(len(x) for x in this.stream_data)
					while read_offset + read_bytes < c_offset + c_length:
						block = this.stream_f.read(131072)

						if not block:
							this.stream_f.close()
							this.stream_f = None
							this.stream_data = []
							break

						this.stream_data.append(block)
						read_bytes += len(block)

						with this.cache_lock:
							this.stream_offset, this.stream_data = this.block_cache.receive_cached_data(
								this.stream_offset, this.stream_data)
				except (HTTPError, IOError) as err:
					if this.stream_f is not None:
						this.stream_f.close()
					this.stream_f = None
					raise IOError(errno.EREMOTEIO, "I/O error: %s" % (str(err),))

	def get_size(this):
		with this.cache_lock:
			return this.block_cache.get_size()

	def get_attr(this):
		return dict(type='file', size=this.get_size())

	def read(this, io, offset, length):
		return this._do_rw(io, offset, length, write=False)

	def write(this, io, offset, data):
		"""
		Write data to file. If *offset* is None, it means append.
		"""
		with this.lock:
			if len(data) > 0:
				this.dirty = True
				if offset is None:
					offset = this.get_size()
				this._do_rw(io, offset, data, write=True)

	def truncate(this, size):
		with this.cache_lock, this.lock:
			if size != this.block_cache.get_size():
				this.dirty = True
			this.block_cache.truncate(size)

	def _buffer_whole_file(this, io):
		with this.cache_lock:
			this._do_rw(io, 0, this.block_cache.get_size(), write=False, no_result=True)

	def upload(this, io, parent_cap=None):
		with this.cache_lock, this.lock:
			# Buffer all data
			this._buffer_whole_file(io)

			# Upload the whole file
			class Fwrapper(object):
				def __init__(this, block_cache):
					this.block_cache = block_cache
					this.size = block_cache.get_size()
					this.f = this.block_cache.get_file()
					this.f.seek(0)
				def __len__(this):
					return this.size
				def read(this, size):
					return this.f.read(size)

			if parent_cap is None:
				upath = this.upath
				iscap = False
			else:
				upath = parent_cap + "/" + ubasename(this.upath)
				iscap = True

			fw = Fwrapper(this.block_cache)
			try:
				filecap = io.put_file(upath, fw, iscap=iscap)
			except (HTTPError, IOError) as err:
				raise IOError(errno.EFAULT, "I/O error: %s" % (str(err),))

			this.info[1]['ro_uri'] = filecap
			this.info[1]['size'] = this.get_size()
			this._save_info()

			this.dirty = False

			return filecap

	def unlink(this):
		with this.cache_lock, this.lock:
			if this.upath is not None and not this.invalidated:
				os.unlink(this.f.path)
				os.unlink(this.f_state.path)
				os.unlink(this.f_data.path)
			this.upath = None


class CachedDirInode(object):
	"""
	Logical file on-disk directory. There should be only a single CachedDirInode
	instance is per each logical directory.
	"""

	def __init__(this, cachedb, upath, io, dircap=None):
		this.upath = upath
		this.closed = False
		this.refcnt = 0
		this.lock = threading.RLock()
		this.invalidated = False

		this.filename, this.key = cachedb.get_filename_and_key(upath)

		try:
			with CryptFile(this.filename, key=this.key, mode='rb') as f:
				this.info = json_zlib_load(f)
			os.utime(this.filename, None)
			return
		except (IOError, OSError, ValueError):
			pass

		f = CryptFile(this.filename, key=this.key, mode='w+b')
		try:
			if dircap is not None:
				this.info = io.get_info(dircap, iscap=True)
			else:
				this.info = io.get_info(upath)
			this.info[1]['retrieved'] = time.time()
			json_zlib_dump(this.info, f)
		except (HTTPError, IOError, ValueError):
			os.unlink(this.filename)
			raise IOError(errno.EREMOTEIO, "failed to retrieve information")
		finally:
			f.close()

	def _save_info(this):
		with CryptFile(this.filename, key=this.key, mode='w+b') as f:
			json_zlib_dump(this.info, f)

	def is_fresh(this, lifetime):
		return (this.info[1]['retrieved'] + lifetime >= time.time())

	def incref(this):
		with this.lock:
			this.refcnt += 1

	def decref(this):
		with this.lock:
			this.refcnt -= 1
			if this.refcnt <= 0:
				this.close()

	def close(this):
		with this.lock:
			this.closed = True

	def listdir(this):
		return list(this.info[1]['children'].keys())

	def get_attr(this):
		return dict(type='dir')

	def get_child_attr(this, childname):
		assert isinstance(childname, str)
		children = this.info[1]['children']
		if childname not in children:
			raise IOError(errno.ENOENT, "no such entry")

		info = children[childname]

		# tahoe:linkcrtime doesn't exist for entries created by "tahoe backup",
		# but explicit 'mtime' and 'ctime' do, so use them.
		ctime = info[1]['metadata'].get('tahoe', {}).get('linkcrtime')
		mtime = info[1]['metadata'].get('tahoe', {}).get('linkcrtime')   # should this be 'linkmotime'?
		if ctime is None:
			ctime = info[1]['metadata']['ctime']
		if mtime is None:
			mtime = info[1]['metadata']['mtime']

		if info[0] == 'dirnode':
			return dict(type='dir', 
						ro_uri=info[1]['ro_uri'],
						rw_uri=info[1].get('rw_uri'),
						ctime=ctime,
						mtime=mtime)
		elif info[0] == 'filenode':
			return dict(type='file',
						size=info[1]['size'],
						ro_uri=info[1]['ro_uri'],
						rw_uri=info[1].get('rw_uri'),
						ctime=ctime,
						mtime=mtime)
		else:
			raise IOError(errno.ENOENT, "invalid entry")

	def unlink(this):
		if this.upath is not None and not this.invalidated:
			os.unlink(this.filename)
		this.upath = None

	def cache_add_child(this, basename, cap, size):
		children = this.info[1]['children']

		if basename in children:
			info = children[basename]
		else:
			if cap is not None and cap.startswith('URI:DIR'):
				info = ['dirnode', {'metadata': {'tahoe': {'linkcrtime': time.time()}}}]
			else:
				info = ['filenode', {'metadata': {'tahoe': {'linkcrtime': time.time()}}}]

		if info[0] == 'dirnode':
			info[1]['ro_uri'] = cap
			info[1]['rw_uri'] = cap
		elif info[0] == 'filenode':
			info[1]['ro_uri'] = cap
			info[1]['size'] = size

		children[basename] = info
		this._save_info()

	def cache_remove_child(this, basename):
		children = this.info[1]['children']
		if basename in children:
			del children[basename]
			this._save_info()


class RandomString(object):
	def __init__(this, size):
		this.size = size

	def __len__(this):
		return this.size

	def __getitem__(this, k):
		if isinstance(k, slice):
			return os.urandom(len(range(*k.indices(this.size))))
		else:
			raise IndexError("invalid index")


def json_zlib_dump(obj, fp):
	try:
		fp.write(zlib.compress(json.dumps(obj).encode('utf-8'), 3))
	except zlib.error:
		raise ValueError("compression error")


def json_zlib_load(fp):
	try:
		return json.load(ZlibDecompressor(fp))
	except zlib.error:
		raise ValueError("invalid compressed stream")


class ZlibDecompressor(object):
	def __init__(this, fp):
		this.fp = fp
		this.decompressor = zlib.decompressobj()
		this.buf = b""
		this.eof = False

	def read(this, sz=None):
		if sz is not None and not (sz > 0):
			return b""

		while not this.eof and (sz is None or sz > len(this.buf)):
			block = this.fp.read(131072)
			if not block:
				this.buf += this.decompressor.flush()
				this.eof = True
				break
			this.buf += this.decompressor.decompress(block)

		if sz is None:
			block = this.buf
			this.buf = b""
		else:
			block = this.buf[:sz]
			this.buf = this.buf[sz:]
		return block


def udirname(upath):
	return "/".join(upath.split("/")[:-1])


def ubasename(upath):
	return upath.split("/")[-1]


# constants for cache score calculation
_DOWNLOAD_SPEED = 1e6  # byte/sec
_LATENCY = 1.0 # sec

def _access_rate(size, t):
	"""Return estimated access rate (unit 1/sec). `t` is time since last access"""
	if t < 0:
		return 0.0
	size_unit = 100e3
	size_prob = 1 / (1 + (size/size_unit)**2)
	return size_prob / (_LATENCY + t)

def cache_score(size, t):
	"""
	Return cache score for file with size `size` and time since last access `t`.
	Bigger number means higher priority.
	"""

	# Estimate how often it is downloaded
	rate = _access_rate(size, t)

	# Maximum size up to this time
	dl_size = _DOWNLOAD_SPEED * max(0, t - _LATENCY)

	# Time cost for re-retrieval
	return rate * (_LATENCY + min(dl_size, size) / _DOWNLOAD_SPEED)


