class Solution:
    def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:
        cars = sorted(zip(position, speed), reverse=True)
        result = 0
        max_time = 0
        for pos, spd in cars:
            time = (target - pos) / spd
            if time > max_time:
                result += 1
                max_time = time
        return result