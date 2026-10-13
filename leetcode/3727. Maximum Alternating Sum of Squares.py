3727. Maximum Alternating Sum of Squares
Medium
Topics
premium lock icon
Companies
Hint
You are given an integer array nums. You may rearrange the elements in any order.

The alternating score of an array arr is defined as:

score = arr[0]2 - arr[1]2 + arr[2]2 - arr[3]2 + ...
Return an integer denoting the maximum possible alternating score of nums after rearranging its elements.

 

Example 1:

Input: nums = [1,2,3]

Output: 12

Explanation:

A possible rearrangement for nums is [2,1,3], which gives the maximum alternating score among all possible rearrangements.

The alternating score is calculated as:

score = 22 - 12 + 32 = 4 - 1 + 9 = 12

Example 2:

Input: nums = [1,-1,2,-2,3,-3]

Output: 16

Explanation:

A possible rearrangement for nums is [-3,-1,-2,1,3,2], which gives the maximum alternating score among all possible rearrangements.

The alternating score is calculated as:

score = (-3)2 - (-1)2 + (-2)2 - (1)2 + (3)2 - (2)2 = 9 - 1 + 4 - 1 + 9 - 4 = 16

 

Constraints:

1 <= nums.length <= 105
-4 * 104 <= nums[i] <= 4 * 104

























































class Solution {
public:
    long long maxAlternatingSum(vector<int>& nums) {
        vector<long long> squares;
        squares.reserve(nums.size());

        for (int x : nums) {
            squares.push_back(1LL * x * x);
        }

        sort(squares.begin(), squares.end());

        int n = squares.size();
        int positiveCount = (n + 1) / 2;
        long long ans = 0;

        for (int i = 0; i < n; i++) {
            if (i < positiveCount) {
                ans += squares[n - 1 - i];
            } else {
                ans -= squares[n - 1 - i];
            }
        }

        return ans;
    }
};






























static const auto harsh = []() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
    return 0;
}();
class Solution {
public:
    long long maxAlternatingSum(vector<int>& nums) {
        int n = nums.size(), i;
        for(int i = 0; i < n; i++) nums[i] = abs(nums[i]);
        nth_element(nums.begin(), nums.begin() + n / 2, nums.end());
        long long res = 0;
        for(i = 0; i < n / 2; i++) res -= nums[i] * nums[i];
        for(; i < n; i++) res += nums[i] * nums[i];
        return res;
    }
};
























class Solution {
public:
    static long long maxAlternatingSum(vector<int>& nums) {
        const int n=nums.size(), h=n/2;
        for(auto& x : nums) x=abs(x);
        nth_element(nums.begin(), nums.begin()+h, nums.end());
        long long ans=0;
        for(int i=0; i<n; i++) 
            ans+=(i<h?-1:1)*(long long)nums[i]*nums[i];
        return ans;
    }
};


















class Solution {
public:
    long long maxAlternatingSum(vector<int>& nums) {
        int n = nums.size();
        for(auto& it: nums) {
            it = it * it;
        }
        sort(nums.begin(), nums.end());
        int c1;
        if(n % 2 == 0)
            c1 = n/2;
        else
            c1 = n/2 + 1;
        int cnt1 = 0;
        bool flag = true;
        long long ans = 0;
        for(int i = n-1; i >= 0; i--) {
            if(cnt1 == c1) {
                flag = false;
            }
            if(flag)
            ans += nums[i];
            else
            ans -= nums[i];
            cnt1++;
        }
        return ans;
    }
};























