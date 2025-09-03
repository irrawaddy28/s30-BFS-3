'''
301 Remove Invalid Parentheses
https://leetcode.com/problems/remove-invalid-parentheses/description/

Given a string s that contains parentheses and letters, remove the minimum number of invalid parentheses to make the input string valid.

Return a list of unique strings that are valid with the minimum number of removals. You may return the answer in any order.

Example 1:
Input: s = "()())()"
Output: ["(())()","()()()"]

Example 2:
Input: s = "(a)())()"
Output: ["(a())()","(a)()()"]

Example 3:
Input: s = ")("
Output: [""]

Constraints:
1 <= s.length <= 25
s consists of lowercase English letters and parentheses '(' and ')'.
There will be at most 20 parentheses in s.

Solution:
1. BFS w/ level info:
We do level-wise BFS removing one character at a time. Thus, at level 1, we remove 1 char, at level 2 we remove 2 chars, and so on.

At the first instance we find a valid expression at some level X, we check for validity of all the strings in the queue at that level (searching for other valid expressions). But we do not go down to the next level X+1 (i.e. we do not add children of of strings at level X) because this would mean X+1 removals of parentheses which is not a minimum.

Note: If len of string = 7 (odd), then at level 1 we have an even number of chars in the string. Then then there is a chance at level 1 to get a valid string. (a valid string has an equal no. of opening and closing parentheses)
At level 2, however, it is guaranteed that no valid string will exist.

Thus, if string len = odd, then valid strings do not exist at even-numbered levels. If string len = even, then valid strings do not exist at odd-numbered levels.
https://youtu.be/5ibsv1HTDyU?t=287
Time: O(2^N), Space: O(2^N * N) - for visited set

2. BFS w/o using level info:
In BFS w/ level approach, although we compute the size of q at each level, we never really used it. Hence, we can eliminate the for loop over size items to get this working.
https://youtu.be/5ibsv1HTDyU?t=2298
Time: O(2^N), Space: O(2^N * N) - for visited set

3. DFS
We do DFS to remove one bracket at a time and track visited strings.
Once we find a valid expression, we check if it's the longest so far.
Only the longest valid strings with the fewest deletions are kept.
Time: O(2^N), Space: O(2^N * N) - for visited set
https://youtu.be/5ibsv1HTDyU?t=2683

'''

from typing import List
from collections import deque

def isValid(s: str) -> bool:
    ''' Time: O(N), Space: O(1) '''
    if not s:
        return True
    N = len(s)
    count = 0
    for i in range(N):
        c = s[i]
        if c == "(":
            count += 1
        elif c == ")":
            count -= 1
            if count < 0: break
        else: # "a"<=c<="z"
            continue

    return count == 0

def removeInvalidParenthesesBFSLevel(s: str) -> List[str]:
    if not s:
        return []
    q = deque()
    h = set()
    result = set()
    q.append(s)
    h.add(s)
    flag = False
    while q and not flag:
        sz = len(q)
        for _ in range(sz):
            curr = q.popleft()
            # check if current string is a valid string
            valid = isValid(curr)
            if valid: # valid
                result.add(curr)
                flag = True
            else: # invalid
                # if all strings in the current level are invalid
                # then flag remains False.
                if flag == False:
                    for j in range(len(curr)):
                        c = curr[j]
                        # if c is a letter, then skip
                        if c >= 'a' and c <= 'z':
                            continue
                        # child = string of all chars of curr except jth char
                        child = curr[0:j] + curr[j+1:]
                        if child not in h:
                            q.append(child)
                            h.add(child)
    return list(result)

def removeInvalidParenthesesBFSNoLevel(s: str) -> List[str]:
    if not s:
        return []
    q = deque()
    h = set()
    result = set()
    q.append(s)
    h.add(s)
    flag = False
    while q:
        curr = q.popleft()
        # check if current string is a valid string
        valid = isValid(curr)
        if valid: # valid
            result.add(curr)
            flag = True
        else: # invalid
            if flag == False:
                for j in range(len(curr)):
                    c = curr[j]
                    # if c is a letter, then skip
                    if c >= 'a' and c <= 'z':
                        continue
                    # child = string of all chars of curr except jth char
                    child = curr[0:j] + curr[j+1:]
                    if child not in h:
                        q.append(child)
                        h.add(child)
    return list(result)

def removeInvalidParenthesesDFS(s: str) -> List[str]:
    def dfs(s):
        nonlocal max_len, result
        # base case
        if len(s) < max_len:
            return

        # logic
        h.add(s)
        if isValid(s):
            if max_len < len(s):
                result = []
                max_len = len(s)
                result.append(s)
            elif max_len == len(s):
                result.append(s)
        else:
             for j in range(len(s)):
                    c = s[j]
                    if c >= 'a' and c <= 'z':
                        continue
                    child = s[0:j] + s[j+1:]
                    if child not in h:
                        dfs(child)

    h = set()
    result = []

    # max len of valid string = string with min no. of parenthesis
    # removals
    max_len = 0
    dfs(s)
    return result

def run_removeInvalidParentheses():
    tests = [("()())()", ["(())()","()()()"]),
             ("(a)())()", ["(a())()","(a)()()"]),
             (")(", [""]),
    ]
    for test in tests:
        s, ans  = test[0], test[1]
        print(f"\nstring (w/ invalid parentheses) = {s}")
        for method in ['bfs_w_level', 'bfs_wo_level', 'dfs']:
            if method == 'bfs_w_level':
                result = removeInvalidParenthesesBFSLevel(s)
            elif method == 'bfs_wo_level':
                result = removeInvalidParenthesesBFSNoLevel(s)
            elif method == 'dfs':
                result = removeInvalidParenthesesDFS(s)
            print(f"Method {method}: result = {result}")
            success = (sorted(ans) == sorted(result))
            print(f"Pass: {success}")
            if not success:
                print(f"Failed")
                return

run_removeInvalidParentheses()