This project is a simplified backend system inspired by IRCTC. It allows users to register, authenticate, search trains, book seats, and view analytics on popular routes.

The system is built using Django and Django REST Framework with MySQL as the primary database and MongoDB for logging and analytics.

User Registers ---> Mysql Stores user data
User logs ig ---> JWT Token Generated
Admin creates Train ---> Mysql stores train
User searches Train ---> Mysql --> Fetch Data
                         MongoDB --> log search
User books Train ---> Mysql --> update seats
                      Mysql --> create Booking
Analytic API ---> MongoDB --> Calculate top routes.
            
