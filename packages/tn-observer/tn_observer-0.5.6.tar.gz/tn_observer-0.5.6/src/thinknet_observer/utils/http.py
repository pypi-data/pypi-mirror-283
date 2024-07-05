
class HttpContext:
    def __init__(self, method: str, route: str, referrer: str, remote_address: str, 
                 duration: float, user_agent: str, url,status_code, ) -> None:
        self.method = method
        self.route = route
        self.referrer = referrer
        self.remote_address = remote_address
        self.duration = duration
        self.user_agent = user_agent
        self.url = url
        self.status_code = status_code