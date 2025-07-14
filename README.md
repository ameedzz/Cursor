# Java Login Page Application

A modern, secure login page built with Spring Boot, Spring Security, and Thymeleaf.

## Features

- 🔐 **Secure Authentication** - Spring Security with BCrypt password encryption
- 🎨 **Modern UI** - Beautiful, responsive design with CSS animations
- 👤 **User Management** - In-memory user store with different roles
- 🛡️ **CSRF Protection** - Built-in security features
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile devices
- ✨ **Professional Styling** - Modern gradient design with smooth transitions

## Demo Credentials

The application comes with pre-configured demo accounts:

- **User Account**: `user` / `password`
- **Admin Account**: `admin` / `admin`

## Prerequisites

- Java 17 or higher
- Maven 3.6+ (or use the Maven wrapper)

## Quick Start

1. **Clone or download the project**

2. **Navigate to the project directory**:
   ```bash
   cd login-app
   ```

3. **Run the application**:
   ```bash
   ./mvnw spring-boot:run
   ```
   
   Or if you have Maven installed:
   ```bash
   mvn spring-boot:run
   ```

4. **Access the application**:
   - Open your browser and go to: `http://localhost:8080`
   - You'll be redirected to the login page at: `http://localhost:8080/login`

## Application Structure

```
src/
├── main/
│   ├── java/com/example/loginapp/
│   │   ├── LoginApplication.java          # Main Spring Boot application
│   │   ├── config/
│   │   │   └── SecurityConfig.java        # Security configuration
│   │   └── controller/
│   │       └── LoginController.java       # Web controllers
│   └── resources/
│       ├── static/css/
│       │   ├── login.css                  # Login page styles
│       │   └── dashboard.css              # Dashboard styles
│       └── templates/
│           ├── login.html                 # Login page template
│           └── dashboard.html             # Dashboard template
└── pom.xml                                # Maven dependencies
```

## Security Features

- **Password Encryption**: BCrypt hashing for secure password storage
- **Session Management**: Automatic session handling with Spring Security
- **CSRF Protection**: Cross-Site Request Forgery protection enabled
- **Authentication Required**: All pages except login require authentication
- **Remember Me**: Optional "Remember Me" functionality
- **Secure Logout**: Proper session invalidation on logout

## Customization

### Adding New Users

Edit `src/main/java/com/example/loginapp/config/SecurityConfig.java` and modify the `userDetailsService()` method:

```java
@Bean
public UserDetailsService userDetailsService() {
    UserDetails newUser = User.builder()
        .username("newuser")
        .password(passwordEncoder().encode("newpassword"))
        .roles("USER")
        .build();
    
    return new InMemoryUserDetailsManager(user, admin, newUser);
}
```

### Styling Changes

- **Login Page**: Modify `src/main/resources/static/css/login.css`
- **Dashboard**: Modify `src/main/resources/static/css/dashboard.css`

### Database Integration

To use a database instead of in-memory users:

1. Add database dependencies to `pom.xml`
2. Create a `UserDetailsService` implementation
3. Configure database connection in `application.properties`

## Technology Stack

- **Spring Boot 3.2.0** - Application framework
- **Spring Security 6** - Authentication and authorization
- **Thymeleaf** - Server-side template engine
- **Maven** - Dependency management and build tool
- **Java 17** - Programming language

## Development

### Running in Development Mode

```bash
./mvnw spring-boot:run -Dspring-boot.run.profiles=dev
```

### Building for Production

```bash
./mvnw clean package
java -jar target/login-app-0.0.1-SNAPSHOT.jar
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions, please create an issue in the project repository.