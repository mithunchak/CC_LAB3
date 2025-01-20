from locust import task, run_single_user, FastHttpUser

class Browse(FastHttpUser):
    host = "http://127.0.0.1:5000"

    default_headers = {
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "DNT": "1",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Upgrade-Insecure-Requests": "1",
    }

    @task
    def browse_page(self):
        """ Perform a GET request to the /browse page """
        with self.client.get(
            "/browse",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                resp.success()
            else:
                resp.failure(f"Failed to load browse page, status code: {resp.status_code}")

if __name__ == "__main__":
    run_single_user(Browse)
