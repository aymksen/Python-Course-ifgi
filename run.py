#!/usr/bin/env python

# donuts
# Given an integer count of a number of donuts, return a string
# of the form 'Number of donuts: <count>', where <count> is the number
# passed in. However, if the count is 10 or more, then use the word 'many'
# instead of the actual count.
# Handles non-integer input by returning an error message.
# So donuts(5) returns 'Number of donuts: 5'
# and donuts(23) returns 'Number of donuts: many'
def donuts(count):
    if isinstance(count, int):
        if count < 10:
            return 'Number of donuts: ' + str(count)
        else:
            return 'Number of donuts: many'
    else:
        return 'Error: Input must be an integer.'

# verbing
# Given a string, if its length is at least 3,
# add 'ing' to its end.
# Unless it already ends in 'ing', in which case
# add 'ly' instead.
# If the string length is less than 3, leave it unchanged.
# Return the resulting string.
def verbing(s):

  if len(s) < 3:
    return s
  else:
    if s.endswith('ing'):
      return s + 'ly'
    else:
      return s + 'ing'

# remove_adjacent
# Given a list of numbers, return a list where
# all adjacent == elements have been reduced to a single element,
# so [1, 2, 2, 3] returns [1, 2, 3]. You may create a new list or
# modify the passed in list.
def remove_adjacent(nums):
  
  if not nums:
    return []

  result_list = [nums[0]]

  for i in range(1, len(nums)):
    if nums[i] != nums[i-1]:
      result_list.append(nums[i])
  return result_list

# --- Provided main() function to test the implementations ---
def main():
  print('donuts')
  # Test cases for donuts function
  print(f"donuts(4) returns: {donuts(4)}")          # Expected: Number of donuts: 4
  print(f"donuts(9) returns: {donuts(9)}")          # Expected: Number of donuts: 9
  print(f"donuts(10) returns: {donuts(10)}")        # Expected: Number of donuts: many
  print(f"donuts('twentyone') returns: {donuts('twentyone')}") # Expected: Error: Input must be an integer.

  print('\nverbing')
  # Test cases for verbing function
  print(f"verbing('hail') returns: {verbing('hail')}")       # Expected: hailing
  print(f"verbing('swiming') returns: {verbing('swiming')}") # Expected: swimingly
  print(f"verbing('do') returns: {verbing('do')}")           # Expected: do

  print('\nremove_adjacent')
  # Test cases for remove_adjacent function
  print(f"remove_adjacent([1, 2, 2, 3]) returns: {remove_adjacent([1, 2, 2, 3])}")       # Expected: [1, 2, 3]
  print(f"remove_adjacent([2, 2, 3, 3, 3]) returns: {remove_adjacent([2, 2, 3, 3, 3])}") # Expected: [2, 3]
  print(f"remove_adjacent([]) returns: {remove_adjacent([])}")                         # Expected: []

# Standard boilerplate to call the main() function.
if __name__ == '__main__':
  main()