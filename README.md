## **Summarizing the completed work:**
1. Developed a simple REST API using FastAPI for a social networking platform.
2. Established interaction between user models and functionalities via FastAPI-powered API endpoints.
3. Utilized a separate environment (e.g., virtualenv) for managing project dependencies and libraries.
4. Implemented authentication method JWT to ensure API security.
5. Designed and implemented key API functionalities, including user registration, post creation, and managing likes.
6. Maintained clean and comprehensible code to enhance readability and maintainability

The project has successfully delivered a scalable and functional REST API for a social networking platform. This API has allowed users to interact with posts via API endpoints, making CRUD operations smooth and seamless. The project also includes an automated bot, which showcases the system's functionalities, highlighting its versatility and usability.

FastAPI, PostgreSQL, and auxiliary libraries have been used during the implementation, displaying the team's commitment to performance, security, and efficient data management.

The architecture and implementation of the project are designed to accommodate future expansion and refinement, providing a solid foundation for future development iterations.
___________

🎞I included a [DEMO VIDEO](https://youtu.be/6_czcgdbpLM) that shows how the bot works. In the video, the bot creates two users, posts, and liked posts on behalf of the users. The number of users, likes, and posts is taken from the configuration file.

To check the `/api/post/analytics/?date_from=2023-12-22&date_to=2023-12-23` route, at the end of the video, I generated a random distribution of new likes per day and demonstrated that the analytics between the selected dates for likes were collected correctly.



## **🔶 Social Network:**

🔹 **Basic models:**
 - User
 - Post (always made by a user)

🔹 **Basic Features:**
 - user signup
 - user login
 - post creation
 - post like
 - post unlike
 - analytics about how many likes was made. Example url /api/analitics/?date_from=2020-02-02&date_to=2020-02-15 . API 
   return analytics aggregated by day.
 - user activity an endpoint which will show when user was login last time and when he mades a last request to the service.

Implemented token authentication (JWT)

## **🔶 Automated bot:**

Repository included a automated bot — object of this bot demonstrate the functionalities of the system according to defined rules. This bot read rules from a config file (JSON), and have following fields:
 - number_of_users
 - max_posts_per_user
 - max_likes_per_user

Bot read the configuration and create this activity:
 - signup users (number provided in config) 
 - each user creates random number of posts with any content (up to max_posts_per_user)
 - After creating the signup and posting activity, posts should be liked
   randomly, posts can be liked multiple times

**🧾 Notes:**

 - Clean and usable REST API
 - Bot this is just separate python script, not a django management command or etc.
 - The project is not detailed. I use my own best judgment for any non-specified requirements, including chosen technology and third-party apps. However,
 - Every decision can be explained and backed by arguments in the interview
