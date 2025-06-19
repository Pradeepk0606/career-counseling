1. https://github.com/

Pythonian/

career_counseling.git

2. Change into the directory of the cloned repo
   ```sh
   cd career_counseling
   ```
3. Setup a Python virtual environment and activate it
   ```sh
   make venv
   env\Scripts\activate

   ```
4. Install project requirements
   ```sh
   make install
   ```
5. Copy and edit environment variables with desired values
   ```sh
   cp .env.example .env
   ```
6. Run database migrations
   ```sh
   make migrate
   ```
7. Create an admin superuser
   ```sh
   make admin
   ```
   _Note: Use `admin` for both the `username` and `password`, and skip entering the `email`. Also type `y` to bypass Password validation._

8. Populate the database with fake data (Optional)
   ```sh
   make populatedb
   ```
9. Run the development server
   ```sh
   make run
   ```
10. Visit the URL in your browser
   ```sh
   127.0.0.1:8000
   ```
   You can also visit the admin dashboard in a new tab and login with the credentials created in step 7.
   ```sh
   127.0.0.1:8000/admin/
   ```

If you went ahead with the optional step (8), you can copy the access code for one of the students here `http://127.0.0.1:8000/admin/career/student/` and use it to access the student assessment dashboard.

## Running Tests

To run tests, run the following command

```bash
   make test
```
