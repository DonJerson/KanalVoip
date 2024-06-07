FROM mysql:latest

# Set environment variables for MySQL
ENV MYSQL_ROOT_PASSWORD=root_password
ENV MYSQL_DATABASE=kamailio
ENV MYSQL_USER=kamailio_user
ENV MYSQL_PASSWORD=kamailio_password

# Expose the MySQL port
EXPOSE 3306

# Copy the database initialization script
COPY ./init.sql /docker-entrypoint-initdb.d/

# Command to run MySQL
CMD ["mysqld"]