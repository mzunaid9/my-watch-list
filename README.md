# to-do-list app
To-Do-List application built with django to Create, Update and Delete tasks.
<br>
<br>
![todolist](https://user-images.githubusercontent.com/65074901/125083144-a5e03900-e0e5-11eb-9092-da716a30a5f3.JPG)


-----
```bash
docker compose up --build --scale app=3 -d
```
----
baseline :

utilisateur simultanés : 50  
Débit (req/s) : Environ 24.8 requêtes par seconde  
Temps de réponse moyen : 17.62 ms   
Temps de réponse p95 : 37 ms  
Taux d'erreur : 0%  

utilisateur simultanés : 100  
Débit (req/s) : Environ 48.7 requêtes par seconde  
Temps de réponse moyen : 23.95 ms  
Temps de réponse p95 : 61 ms   
Taux d'erreur : 0%  

Utilisateurs simultanés : 200  
Débit (req/s) : Environ 99.7 r/s   
Temps de réponse moyen : 41.6 ms   
Temps de réponse p95 : 120 ms  
Taux d'erreur : 0%

------
N-instances :  
Utilisateurs simultanés : 50   
Débit (RPS) : 24.7 r/s   
Temps de réponse moyen : 32.45  
Temps de réponse p95 : 62 ms   
Taux d'erreur : 0%  

Utilisateurs simultanés : 100  
Débit (RPS) : 48.3 r/s     
Temps de réponse moyen : 63 ms 
Temps de réponse p95 : 180 ms  
Taux d'erreur : 0%  


Utilisateurs simultanés : 200    
Débit (RPS) : 73.1 r/s    
Temps de réponse moyen : 822.94 ms  
Temps de réponse p95 : 1900 ms    
Taux d'erreur : 0%    

------
ex 4 :  
Utilisateurs simultanés : 50  
Débit (RPS) : 25.3 r/s  
Temps de réponse moyen : 18.12 ms  
Temps de réponse p95 : 38 ms  
Taux d'erreur : 41%  


Utilisateurs simultanés : 100  
Débit (RPS) : 49.6 r/s   
Temps de réponse moyen : 19.45 ms   
Temps de réponse p95 : 44 ms   
Taux d'erreur : 43%  

Utilisateurs simultanés : 200   
Débit (RPS) : 98.7 r/s   
Temps de réponse moyen : 34.94 ms   
Temps de réponse p95 : 110 ms   
Taux d'erreur : 44%   