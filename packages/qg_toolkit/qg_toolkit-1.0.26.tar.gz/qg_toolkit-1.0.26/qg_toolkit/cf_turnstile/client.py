import flask

from qg_toolkit.cf_turnstile.cf_turnstile import CFTurnstileSolver


class CFTurnstileSolverClient:
    def __init__(self, site_key: str, target_url: str, headless: bool = True, proxy: str = None):
        self.cf_solve = CFTurnstileSolver(site_key, target_url, headless=headless, proxy=proxy)
        self.app = flask.Flask(__name__)
        self.add_routes()

    def __del__(self):
        self.cf_solve.close_browser()

    def start(self, port=5000):
        self.app.run(host='0.0.0.0', port=port)

    def add_routes(self):
        @self.app.route("/")
        def index():
            return flask.redirect("https://pioneer.particle.network/zh-CN/point")

        @self.app.route("/solve", methods=["POST"])
        def solve():
            # 解决逻辑放在这里
            token = self.cf_solve.solve()
            print(f"[CF_TOKEN]破解成功: {token}")
            return make_response(token)

        def make_response(captcha_key):
            if captcha_key == "failed":
                return flask.jsonify({"status": "error", "token": None})
            return flask.jsonify({"status": "success", "token": captcha_key})


if __name__ == '__main__':
    site_key = '0x4AAAAAAAaHm6FnzyhhmePw'
    target_url = 'https://pioneer.particle.network/zh-CN/nft'
    # cf_solve = CFTurnstileSolver(site_key, target_url, headless=True)
    # for i in range(10):
    #     cf_token = cf_solve.solve()
    #     print(f'CF_TOKEN破解【{i + 1}】: {cf_token}')
    # cf_solve.close_browser()
    client = CFTurnstileSolverClient(site_key, target_url, headless=True)
    client.start(port=5555)