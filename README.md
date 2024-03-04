# Purpose

This project is a demonstration of building a secure API using Flask, implementing advanced authentication mechanisms such as OAuth2 and JWT. The API provides endpoints for user data retrieval and manipulation while ensuring robust security features and efficient handling of user credentials and access tokens.

## Objectives:

1. **Advanced Authentication and API Development:**
   Develop a secure API using Flask that supports OAuth2 and JWT for authentication. Your API should demonstrate advanced security features and efficient handling of user credentials and access tokens.

2. **Complex Data Relationship Handling:**
   Design and implement a data model capable of managing complex relationships. Utilize Firestore to showcase your ability to manipulate and query data efficiently, ensuring integrity and performance.

3. **Real-time Data Processing:**
   Implement a feature using WebSockets that allows for real-time data processing and communication. This feature should highlight your ability to handle concurrent data streams and provide a seamless user experience.

4. **Machine Learning Model Integration:**
   Integrate a pre-trained machine learning model into your application using PyTorch. Demonstrate your application's ability to interact with the model, process inputs, and display outputs in a meaningful way.

5. **API Rate Limiting and Caching:**
   Implement rate limiting and caching mechanisms to optimize the performance of your API. Your solution should demonstrate an understanding of how to manage and scale API requests efficiently.

## Submission Guidelines:

Your submission should be organized within a GitHub repository containing:

- Complete source code with detailed comments and documentation.
- A comprehensive README file that includes setup instructions, how to run the application, and a guide to navigating your codebase.
- A written overview discussing your design choices, the challenges you faced, and how you overcame them.

# Setups:

## Creating a Google Project in the Organization

The first step in setting up a Google project within your organization involves creating a project on the Google Cloud Platform (GCP). Follow these initial steps to get started:

1. **Navigate to Google Cloud Console:**
   Access the Google Cloud Console by visiting [console.cloud.google.com](https://console.cloud.google.com/).

2. **Sign in to Your Google Account:**
   Sign in with the Google account associated with your organization's GCP access.

3. **Create a New Project:**
   Once logged in, click on the project dropdown menu located at the top of the console. Then, select "New Project" to initiate the project creation process.

4. **Enter Project Details:**
   Provide a name for your project, ensuring it accurately represents its purpose within your organization. Optionally, you can assign a unique project ID, which will be used in the project's URLs.

5. **Choose Organization:**
   If your organization uses Google Workspace (formerly G Suite), you may have the option to associate the project with your organization. Select the appropriate organization from the dropdown menu if prompted.

6. **Review and Confirm:**
   After entering project details, review the information to ensure accuracy. Once confirmed, click on the "Create" button to proceed.

7. **Wait for Project Creation:**
   Google will now create your project. This process may take a few moments. Once completed, you'll be directed to the project dashboard.

## Creating Connections and Credentials

Now that your project is set up, the next step involves creating API connections and credentials to enable authentication and access control. Follow the steps outlined in the [Google documentation](https://developers.google.com/identity/protocols/oauth2) for detailed instructions on setting up OAuth 2.0 authentication and obtaining the necessary credentials.

Here's a brief overview of the process:

1. **Set Up OAuth Consent Screen:**
   Configure the OAuth consent screen to define how your application will be presented to users and obtain their consent for accessing their data. Provide necessary details such as application name, logo, and privacy policy URL.

2. **Create OAuth Client ID:**
   Generate OAuth 2.0 client credentials (Client ID and Client Secret) to authenticate your application with Google APIs. Configure the OAuth client ID settings according to your application's requirements, specifying authorized redirect URIs (MAKE SURE TO USE THIS ADDRESS: "http://127.0.0.1:5001/login/google/authorized") and other relevant details.

## Saving Client ID and Client Secret in a .env File

To securely store your OAuth 2.0 client credentials (Client ID and Client Secret), follow these steps:

1. **Copy Credentials to Sample .env File:**
   Copy your Client ID and Client Secret into a file named `.env`, structured as follows:
   ```plaintext
   CLIENT_ID=your_client_id_here
   CLIENT_SECRET=your_client_secret_here
    ```
2. **Rename File to .env:**
    Rename the `sample.env` file to `.env`. This ensures that your sensitive credentials are securely stored in an environment file that can be accessed by your application.

By following these steps, you can securely store and manage your OAuth 2.0 client credentials in a `.env` file within your project. Remember to keep this file private and not share it publicly or commit it to version control.

## Creating a Firebase Firestore Cloud Database for Python

1. **Set Up Firebase Project:**
   Start by creating a new project or selecting an existing one in the Firebase console (console.firebase.google.com).

2. **Enable Firestore:**
   Once your project is set up, navigate to the "Firestore Database" section in the Firebase console. Click on "Create Database" and choose the location for your Firestore instance.

3. **Generate Service Account Key:**
    In the Firebase console, go to "Project Settings > Service Accounts" and click on "Generate New Private Key". This will download a JSON file containing your service account credentials.

4. **Set Up .env File:**
    Change the `.env` file in your project directory and assign the path to the downloaded JSON file to the variable named `fire_json`. For example:
    ```plaintext
    fire_json=/path/to/serviceAccountKey.json
    ```
    
## Building and Running a Docker Image

1. **Navigate to Project Directory:**
   Open a terminal or command prompt and navigate to the directory containing your Dockerfile and project files.

2. **Build Docker Image:**
   Run the following command to build the Docker image:
    ```
    docker build -t purpose .
    ```

3. **Run Docker Container:**
    After the Docker image is built successfully, you can run it in a Docker container. Use the following command to run the container, mapping port 5001 on the host to port 5001 on the container:
    ````
    docker run -p 5001:5001 purpose
    ````

4. **Access Your Application:**
    Once the container is running, you can access your application by navigating to `http://localhost:5001` in your web browser. The application should now be running on port 5001 inside the Docker container.

### Adding Initial Data to Firestore Database

If you wish to add initial data to your Firestore database, you can run the `firestore_methods.py` file located in the `utils` folder. Follow these steps:

1. **Ensure Required Packages are Installed:**
   Before running the script, make sure that the `firebase_admin` and `dotenv` packages are installed in your Python environment. You can install them using pip:
   ```bash
   pip install firebase_admin python-dotenv
   ```
2. **Navigate to the Utils Folder:**
   Open a terminal or command prompt and navigate to the directory where your firestore_methods.py file is located. If it's within a folder named utils, navigate to that folder.

3. **Run the Script:**
   Execute the script by running the following command:
   ```
   python firestore_methods.py
   ```
4. **Verify Data Addition:**
   Once the script completes execution, verify that the initial data has been successfully added to your Firestore database by checking the Firestore console or querying the database programmatically.

# Issues and considerations:

## Choosing the Better Database Construction

### Embedding `posts` Collection within `users` Collection

Embedding the `posts` collection within the `users` collection offers several advantages:

- **Simplified Queries:** It simplifies queries when accessing a user's posts since posts are directly nested within the user document. This reduces the number of reads needed and improves query efficiency.

- **Optimized Access:** Users can easily access their posts with a single read operation, which is beneficial for applications where posts are always accessed in the context of a user.

### Keeping `posts` Collection Separate

Alternatively, keeping the `posts` collection separate allows for more flexibility and scalability:

- **Independent Access:** Posts can be accessed independently of users, which is useful if posts need to be queried globally or if they have relationships with entities besides users.

- **Structured Management:** It facilitates managing posts in a more structured manner, especially when posts have complex relationships with other entities.

- **Avoiding Scalability Issues:** Keeping the `posts` collection separate can prevent potential scalability issues, especially if a user has a large number of posts, as Firestore documents have size limits.

### The Second Option Is the Way to Go

Opting for the second option is advantageous due to its scalability. It acknowledges the potential for posts to originate from sources beyond just individual users, such as pages. By accommodating this flexibility, the system becomes more adaptable to future changes and expansions in the platform's functionality. This ensures robustness and effectiveness in managing posts across diverse content sources, enhancing overall reliability.
