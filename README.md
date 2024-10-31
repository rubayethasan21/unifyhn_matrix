# unifyhn_matrix - Matrix Server for HNUnisync

**unifyhn_matrix** is the Matrix server backend for **HNUnisync.de**, enabling seamless communication between students and instructors through Matrix rooms created from ILIAS course enrollments. It automates the creation and management of Matrix rooms, providing a scalable communication platform for educational institutions.

## Key Features

- **Matrix Protocol Integration**: Synchronizes ILIAS courses with Matrix rooms to facilitate real-time communication between students and instructors.
- **Automated Room Creation**: Automatically creates Matrix rooms based on course enrollments and invites students to the appropriate rooms.
- **Secure User Authentication**: Users log in using Matrix credentials, ensuring that access to communication channels is restricted to authorized participants.
- **Supports Multiple Matrix-Based Messaging Clients**: Users can join rooms using any Matrix client, such as **Element** or **FluffyChat**, for a seamless communication experience.

## Technologies Used

- **Matrix-Nio**: Python library for interacting with the Matrix protocol.
- **Quart**: For building asynchronous web services.
- **Matrix-Synapse**: The primary server software for running the Matrix communication server.
- **Requests**: For making HTTP requests during server interactions.
- **Python**: Core programming language used for development.

## Prerequisites

- **Python 3.8+**
- **Matrix-Synapse**: Ensure that the Matrix-Synapse server is installed and configured. Refer to the [Matrix Synapse documentation](https://matrix-org.github.io/synapse/latest/setup/installation.html) for setup instructions.

## Installation & Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/rubayethasan21/unifyhn_matrix.git
   cd unifyhn_matrix
   ```

2. **Setup the initaial project, installing and running Matrix Server by running a setup.sh file**:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Matrix server configuration**:
   Configure the following environment variables to connect with the Matrix Synapse server:
   - Update homeserver.yaml file as the configuration written in the homeserver_unifyhn.yaml file
   


4. **Re Start the Matrix Server**:
   ```bash
   synctl restart
   synctl start
   synctl stop
   ```
5. **Verify the Server Status**:
   Ensure that your Matrix Synapse server is running properly and that the integration service can communicate with it.

## Usage

- **Automatic Room Creation**: Once the integration service is running, it listens for requests from the **HNUnisync** application to create and manage Matrix rooms.
- **User Invitations**: Students enrolled in ILIAS courses are automatically invited to the respective Matrix rooms.
- **Join Matrix Rooms**: Students and instructors can use their preferred Matrix-based messaging applications (e.g., **Element**, **FluffyChat**) to join the rooms and engage in discussions.

## Contributing

Contributions are welcome! To contribute to the project, please follow these steps:

1. **Fork the repository**.
2. **Create a new branch** for your feature or bugfix (`git checkout -b feature-name`).
3. **Make your changes** and **commit them** (`git commit -m 'Add a new feature'`).
4. **Push the branch** to your fork (`git push origin feature-name`).
5. **Submit a pull request** to the `main` branch of the original repository.

## Contact

For support or inquiries, please open an issue on the GitHub repository or reach out to the repository owner.

## Links

- Matrix Server URL: [https://unifyhn.de](https://unifyhn.de)
- GitHub Repository: [https://github.com/rubayethasan21/unifyhn_matrix](https://github.com/rubayethasan21/unifyhn_matrix)
