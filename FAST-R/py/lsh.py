'''
This is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This software is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this source.  If not, see <http://www.gnu.org/licenses/>.
'''

from collections import defaultdict
from collections import OrderedDict
import itertools

import xxhash

"""
This files contains implementations of shingling, minwise hashing, 
and locality sensitive hashing techniques.
All techniques are adapted to be used as part of FAST test case 
prioritization algorithms.
"""

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# SHINGLING

# return the k-shingles of an input test suite.
def kShingles(TS, k):
	"""INPUT
	(dict)TS: key=tcID, value=(set of entities)
	(int)k: size of k-shingles

	OUTPUT
	(dict)shingles: key=tcID, value=set of k-shingles of test case ID"""
	shingles = OrderedDict()
	for tcID in TS:
		tc = TS[tcID]
		shingle = set()
		for i in range(len(tc) - k + 1):
			shingle.add(hash(tc[i:i + k]))
		shingles[tcID] = shingle

	return shingles


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# MINWISEHASHING

# generate a family of hash functions
def hashFamily(i):
	def hashMember(x):
		return xxhash.xxh64(x, seed=37 * (2 * i + 1)).hexdigest()

	return hashMember

# compute minhashing of a single test case
def tcMinhashing(test_case, hash_functions):
	"""INPUT
	(pair)test_case: (tcID, set of entities)
	(list(fun))hash_functions: list of hash_functions

	OUTPUT
	(list)tc_signature: list of minhash values (signature)
	"""
	n = len(hash_functions)
	tc_ID, tc_shingles = test_case
	# initialized to max_value ('ffffffff') to correctly compute the min
	tc_signature = ["ffffffff" for i in range(n)]
	for tc_shingle in tc_shingles:
		for i in range(n):
			tc_hash = hash_functions[i](str(tc_shingle))
			if tc_hash < tc_signature[i]:
				tc_signature[i] = tc_hash

	return tc_signature


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# LOCALITY SENSITIVE HASHING (LSH)

# implement the LSH bucket for fast similarity-based search
def LSHBucket(minhashes, b, r, n):
	"""INPUT
	(dict)minhashes: key=minhashes of test cases
	(int)b: number of bands
	(int)r: number of rows
	(int)n: number of hash functions (n = b*r)

	OUTPUT
	(dict(dict))LSHBuckets: key=band, val=dict(key=col_sig, val=set(tc_IDs))"""
	assert(b * r == n)

	# key=band, val=dict(key=col_sig, val=set(tc_IDs))
	bucket = defaultdict(dict)
	i = 0
	while i < n:  # for each band
		bucket[i] = defaultdict(set)  # to catch collisions in each band
		for tc_signature in minhashes:
			tc_ID, signatures = tc_signature
			column = signatures[i:i + r]
			column_signature = hash(str(column))

			bucket[i][column_signature].add(tc_ID)

		i += r  # next band

	return bucket

# return the set of possibly similar test cases using LSH bucket
def LSHCandidates(bucket, signature, b, r, n):
	"""INPUT
	(dict)bucket: key=band, val=dict(key=col_sig, val=set(tc_IDs))
	(pair)signature: (0, minhash)
	(int)b: number of bands
	(int)r: number of rows
	(int)n: number of hash functions (n = b*r)

	OUTPUT
	(set)candidates: set of possibly similar test cases"""
	assert(b * r == n)

	candidates = set()

	i = 0
	while i < n:  # for each band
		tc_ID0, minhash = signature
		column = minhash[i:i + r]
		column_signature = hash(str(column))

		for tc_ID in bucket[i][column_signature]:
			candidates.add(tc_ID)

		i += r  # next band

	return candidates


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# JACCARD SIMILARITY/DISTANCE EXACT AND ESTIMATES

# exact jaccard similarity
def jSimilarity(a, b):
	return float(len(a & b)) / len(a | b)

# exact jaccard distance
def jDistance(a, b):
	return 1.0 - jSimilarity(a, b)

# estimate jaccard similarity using minhashing
def jSimilarityEstimate(s1, s2):
	assert(len(s1) == len(s2))
	return sum([1 for i in range(len(s1)) if s1[i] == s2[i]]) / float(len(s1))

# estimate jaccard distance using minhashing
def jDistanceEstimate(s1, s2):
	return 1.0 - jSimilarityEstimate(s1, s2)
