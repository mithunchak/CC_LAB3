from locust import task, run_single_user, FastHttpUser
from insert_product import login

class AddToCart(FastHttpUser):
    host = "http://127.0.0.1:5000"
    username = "test123"
    password = "test123"

    default_headers = {
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "DNT": "1",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
    }

    def on_start(self):
        """ This method is executed once at the beginning of the test. """
        cookies = login(self.username, self.password)
        self.token = cookies.get("token")
        # Add token to the default headers
        self.default_headers["Cookies"] = f"token={self.token}"

    @task
    def t(self):
        """ Perform a GET request to the /cart endpoint """
        with self.client.get(
            "/cart",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                resp.success()
            else:
                resp.failure(f"Failed to load cart, status code: {resp.status_code}")

if __name__ == "__main__":
    run_single_user(AddToCart)
