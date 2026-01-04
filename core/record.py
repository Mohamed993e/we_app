import datetime

# Example usage
class Record:
    def __init__(self, total: float, used: float, remain: float, effectiveTime: int, expireTime: int):
        self.total = total
        self.used = used
        self.remain = remain
        self.effectiveTime = effectiveTime
        self.expireTime = expireTime
        self.time = datetime.datetime.now()
        
    def get_secounds_left(self) -> int:
        # Calculate seconds left until expiry
        current_time = datetime.datetime.now()
        delta =current_time - self.time 
        return int(delta.total_seconds())
    @staticmethod
    def from_json(json_data: dict) -> 'Record':
        # Assuming json_data contains the relevant structure as per the original JSON
        body = json_data['body'][0]
        
        # Extract data from the body
        total = body['total']
        used = body['used']
        remain = body['remain']
        effectiveTime = body['effectiveTime']
        expireTime = body['expireTime']
        
        # Create Record object
        return Record(total, used, remain, effectiveTime, expireTime)
    def convert_timestamp(self, timestamp: int) -> str:
        # Convert Unix timestamp (milliseconds) to a human-readable date
        return datetime.datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
    @property
    def get_effective_time(self) -> str:
        # Convert and return effective time
        return self.convert_timestamp(self.effectiveTime)
    @property
    def get_expire_time(self) -> str:
        # Convert and return expire time
        return self.convert_timestamp(self.expireTime)
    def __str__(self) -> str:
        # Override __str__ to provide a more user-friendly string representation
        return (f"Record Details:\n"
                f"  Total: {self.total} GB\n"
                f"  Used: {self.used} GB\n"
                f"  Remaining: {self.remain} GB\n"
                f"  Effective Time: {self.get_effective_time}\n"
                f"  Expiry Time: {self.get_expire_time}\n")
