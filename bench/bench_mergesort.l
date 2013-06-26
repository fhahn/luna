--[[ 
    Implementation of MergeSort
    taken from https://gist.github.com/biomood/1132659, slightly modified
--]]



-- main mergesort algorithm
function mergeSort(A, p, r)
        -- return if only 1 element
    if p < r then
        local q = math.floor((p + r)/2)
        mergeSort(A, p, q)
        mergeSort(A, q+1, r)
        merge(A, p, q, r)
    end
end

-- merge an array split from p-q, q-r
function merge(A, p, q, r)
    local n1 = q-p+1
    local n2 = r-q
    local left = {}
    local right = {}
    for i=1, n1 do
        left[i] = A[p+i-1]
    end
    for i=1, n2 do
        right[i] = A[q+i]
    end
    
    left[n1+1] = math.huge
    right[n2+1] = math.huge
    
    local i=1
    local j=1
    
    for k=p, r do
        if left[i]<=right[j] then
            A[k] = left[i]
            i=i+1
        else
            A[k] = right[j]
            j=j+1
        end
    end
end

function reverseArray(A)
    for i=1, 200000 do
        A[i] = 200000 - i
    end
end

-- print all the elements in the array A
function printArray(A)
    --s = table.concat(A, ", ")
    s = ""
    for i=1, #A do
        s = s .. ", " .. A[i]
    end
    print(s)
end

-- create the original array
A = {}
reverseArray(A)

--print("Original Array")
--printArray(A)
--print("\n")

-- sort the array
mergeSort(A, 1, #A)
--print("Sorted Array")
--printArray(A)
assert(A[1] <= A[2] and A[2] <= A[3] and A[3] <= A[4] and A[5] <= A[6])
