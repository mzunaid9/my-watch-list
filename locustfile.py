from locust import HttpUser, task, between

class WatchlistUser(HttpUser):
    # 1 et 3 secondes entre chaque action
    wait_time = between(1, 3)

    def on_start(self):
        """Action exécutée au lancement : on se connecte (à adapter selon tes URLs de login J1)"""
        pass

    @task(3)
    def view_watchlist(self):
        """Consulter sa watchlist (action fréquente)"""
        self.client.get("/") 

    @task(1)
    def view_login_page(self):
        """Naviguer vers la page de connexion"""
        self.client.get("/login/")