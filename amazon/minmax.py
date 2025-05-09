def findMinimumMaximum(parcels, extra_parcels):
    current_max = max(parcels)
    # Debug prints matching the Rust code:
    print(f"Left Boundary: {max(parcels)}")
    print(f"Right Boundary: {extra_parcels}")

    # Set the binary search bounds
    left = current_max
    right = current_max + extra_parcels

    iters = 0
    while left < right:
        mid = left + (right - left) // 2
        print("--------------------------------------Next Iteration--------------------------------------")
        print(f"amount of possible optimal values left={right - left}")
        print(f"Iteration {iters}: left={left}, right={right}, mid={mid}")
        needed_parcels = 0
        for parcel in parcels:
            parcel_count = parcel
            if parcel_count < mid:
                needed_parcels += (mid - parcel_count)

        print(f"After looping through the array of parcels the amount we would need to add is {needed_parcels}")
        if needed_parcels >= extra_parcels:
            print(f"This value is greater than or equal to the amount of extra parcels we have, so it's closer, thus we'll set the next upper bound to {mid}")
            # We have room to place all extra parcels at or below 'mid'
            # so try lowering 'mid'
            right = mid
        else:
            print(f"This value is less than the amount of extra parcels we have, so we need to increase it, thus we'll set the next lower bound to {mid + 1}")
            # We can't distribute all extras if we cap at 'mid'
            # so increase it
            left = mid + 1
        iters += 1

    return left


out = findMinimumMaximum([7,5,1,9,1,0,10,9], 215)
print(f"Final Result: {out}")

