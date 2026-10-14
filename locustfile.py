from locust import HttpUser, task, between

class WatchlistUser(HttpUser):
    # 1 et 3 secondes entre chaque action
    wait_time = between(1, 3)

    def on_start(self):
        """Action exécutée au lancement"""
        pass

    @task(3)
    def view_watchlist(self):
        """Consulter sa watchlist (action fréquente)"""
        self.client.get("/") 

    @task(1)
    def view_login_page(self):
        """Naviguer vers la page de connexion"""
        self.client.get("/login/")

    @task(2)
    def add_netflix_shows(self):
        """Simule l'ajout de séries Netflix (appelle l'API TMDB mise en cache dans Redis)"""
        self.client.post("/add/netflix/")

    @task(1)
    def add_amazon_shows(self):
        """Simule l'ajout de séries Amazon Prime"""
        self.client.post("/add/amazon/")