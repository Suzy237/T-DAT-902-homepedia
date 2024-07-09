# Use the official PHP image with PHP-FPM
FROM php:8.2-fpm

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    libpng-dev \
    libpq-dev \
    libonig-dev \
    libxml2-dev \
    zip \
    unzip \
    nginx \
    python3 \
    python3-pip \
    python3-requests \
    procps \
    openjdk-17-jdk \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Add Java bin to PATH
ENV PATH="/usr/lib/jvm/java-17-openjdk-amd64/bin:${PATH}"

# Make it possible to run pip3
RUN mv /usr/lib/python3.11/EXTERNALLY-MANAGED /usr/lib/python3.11/EXTERNALLY-MANAGED.old

# Install pyspark
RUN pip3 install pyspark

# Install PHP extensions
RUN docker-php-ext-install pdo_pgsql mbstring exif pcntl bcmath gd

# Install MongoDB extension
RUN pecl install mongodb && echo "extension=mongodb.so" > $PHP_INI_DIR/conf.d/mongo.ini

# Install Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Set working directory
WORKDIR /var/www

# Copy existing application directory contents
COPY . /var/www

# Copy existing application directory permissions
COPY --chown=www-data:www-data . /var/www

# Install Composer dependencies
RUN composer install --no-interaction --prefer-dist --optimize-autoloader

# Nginx configuration
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

# Install Node.js
RUN curl -sL https://deb.nodesource.com/setup_20.x | bash -
RUN apt-get install -y nodejs

# Install npm packages
RUN npm install && npm run build

# Fix permissions
RUN chown -R www-data:www-data storage bootstrap/cache
RUN chmod -R 775 storage bootstrap/cache

RUN curl -o /var/www/python_scripts/postgresql-42.7.3.jar https://jdbc.postgresql.org/download/postgresql-42.7.3.jar

# Expose ports for Nginx and PHP-FPM
EXPOSE 80

# Start Nginx and PHP-FPM
CMD service nginx start && php-fpm
