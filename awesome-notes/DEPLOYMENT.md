# Awesome Notes - Deployment Guide

## Table of Contents
- [Local Development Setup](#local-development-setup)
- [Database Migrations](#database-migrations)
- [AWS Production Deployment](#aws-production-deployment)
- [Environment Configuration](#environment-configuration)
- [Troubleshooting](#troubleshooting)

## Local Development Setup

### Prerequisites
- Docker Desktop installed and running
- Git

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/chrisgrobauskas/chrisgrobauskas.github.io.git
   cd chrisgrobauskas.github.io/awesome-notes
   ```

2. **Start the application with Docker**
   ```bash
   docker-compose up --build
   ```

   This command will:
   - Build and start PostgreSQL database
   - Build and start Flask backend on http://localhost:5000
   - Build and start Angular frontend on http://localhost:4200

3. **Access the application**
   - Open your browser to http://localhost:4200
   - Create a new account
   - Start taking notes!

4. **Stop the application**
   ```bash
   docker-compose down
   ```

### Manual Setup (Without Docker)

If you prefer to run services individually:

#### Backend Setup

```bash
cd awesome-notes/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your PostgreSQL connection string

# Initialize database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Run the server
python run.py
```

#### Frontend Setup

```bash
cd awesome-notes/frontend

# Install dependencies
npm install

# Run development server
ng serve
```

## Database Migrations

### Creating a New Migration

When you modify the database models:

```bash
cd awesome-notes/backend
source venv/bin/activate
flask db migrate -m "Description of your changes"
flask db upgrade
```

### Applying Migrations

```bash
flask db upgrade
```

### Rolling Back Migrations

```bash
flask db downgrade
```

## AWS Production Deployment

### Prerequisites

1. **AWS Account** with appropriate permissions
2. **AWS CLI** installed and configured
3. **PostgreSQL RDS Instance** (for production database)
4. **S3 Bucket** (for frontend hosting)
5. **CloudFront Distribution** (for CDN)

### Backend Deployment (AWS Lambda via Zappa)

1. **Configure AWS credentials**
   ```bash
   aws configure
   ```

2. **Set up RDS PostgreSQL Database**
   - Create a PostgreSQL RDS instance in AWS Console
   - Note the connection string

3. **Configure Zappa**
   ```bash
   cd awesome-notes/backend
   cp zappa_settings.example.json zappa_settings.json
   ```
   
   Edit `zappa_settings.json`:
   ```json
   {
     "production": {
       "app_function": "run.app",
       "aws_region": "us-east-1",
       "runtime": "python3.9",
       "s3_bucket": "your-zappa-bucket-name",
       "environment_variables": {
         "FLASK_ENV": "production",
         "DATABASE_URL": "postgresql://user:pass@rds-endpoint:5432/dbname",
         "SECRET_KEY": "your-production-secret-key",
         "JWT_SECRET_KEY": "your-jwt-secret-key"
       }
     }
   }
   ```

4. **Deploy**
   ```bash
   zappa deploy production
   ```
   
   Or update existing deployment:
   ```bash
   zappa update production
   ```

5. **Run database migrations on Lambda**
   ```bash
   zappa manage production "flask db upgrade"
   ```

### Frontend Deployment (S3 + CloudFront)

1. **Create S3 Bucket**
   ```bash
   aws s3 mb s3://your-frontend-bucket-name
   ```

2. **Configure bucket for static website hosting**
   ```bash
   aws s3 website s3://your-frontend-bucket-name/ \
     --index-document index.html \
     --error-document index.html
   ```

3. **Create CloudFront Distribution**
   - Go to AWS Console → CloudFront
   - Create a new distribution pointing to your S3 bucket
   - Configure SSL certificate (optional but recommended)
   - Note the distribution ID

4. **Update frontend environment**
   
   Edit `awesome-notes/frontend/src/environments/environment.ts`:
   ```typescript
   export const environment = {
     production: true,
     apiUrl: 'https://your-lambda-api-url.amazonaws.com/api'
   };
   ```

5. **Build and deploy**
   ```bash
   cd awesome-notes/frontend
   npm run build -- --configuration production
   
   aws s3 sync dist/awesome-notes s3://your-frontend-bucket-name --delete
   
   aws cloudfront create-invalidation \
     --distribution-id YOUR_DISTRIBUTION_ID \
     --paths "/*"
   ```

### GitHub Actions Secrets

Configure the following secrets in your GitHub repository settings:

**Backend Deployment:**
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `PRODUCTION_DATABASE_URL`
- `SECRET_KEY`
- `JWT_SECRET_KEY`

**Frontend Deployment:**
- `AWS_ACCESS_KEY_ID` (same as above)
- `AWS_SECRET_ACCESS_KEY` (same as above)
- `S3_BUCKET_NAME`
- `CLOUDFRONT_DISTRIBUTION_ID`
- `PRODUCTION_API_URL`

## Environment Configuration

### Backend Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `FLASK_APP` | Flask application entry point | `run.py` |
| `FLASK_ENV` | Environment (development/production) | `development` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@localhost:5432/dbname` |
| `SECRET_KEY` | Flask secret key | Random string |
| `JWT_SECRET_KEY` | JWT signing key | Random string |

### Frontend Environment Variables

Edit `src/environments/environment.ts`:

```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:5000/api'  // Backend API URL
};
```

## Troubleshooting

### Docker Issues

**Problem: Port already in use**
```bash
# Find and kill process using port 5000
lsof -ti:5000 | xargs kill -9

# Or change the port in docker-compose.yml
```

**Problem: Database connection failed**
```bash
# Check if PostgreSQL is running
docker-compose ps

# View logs
docker-compose logs postgres
```

### Backend Issues

**Problem: Import errors**
```bash
# Make sure you're in the virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

**Problem: Database migrations fail**
```bash
# Reset migrations (CAUTION: This will delete data)
flask db downgrade base
rm -rf migrations
flask db init
flask db migrate
flask db upgrade
```

### Frontend Issues

**Problem: Module not found**
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Problem: Build fails**
```bash
# Check TypeScript errors
ng build --configuration development
```

### CORS Issues

If you see CORS errors in the browser console:

1. **Backend:** Verify Flask-CORS is configured correctly in `app/__init__.py`
2. **Frontend:** Check that `apiUrl` in environment.ts matches your backend URL
3. **Production:** Configure CORS origins in Flask app to include your CloudFront domain

### Common AWS Deployment Issues

**Problem: Zappa deployment fails**
```bash
# Check IAM permissions
# Ensure your AWS user has Lambda, S3, and API Gateway permissions

# Check Python version
python --version  # Should be 3.9

# View Zappa logs
zappa tail production
```

**Problem: Database connection timeout on Lambda**
- Check VPC configuration
- Ensure Lambda function is in same VPC as RDS
- Verify security group rules allow connection

**Problem: CloudFront shows old content**
```bash
# Invalidate CloudFront cache
aws cloudfront create-invalidation \
  --distribution-id YOUR_DIST_ID \
  --paths "/*"
```

## Security Best Practices

1. **Never commit secrets** to version control
2. **Use strong passwords** for production databases
3. **Enable SSL/TLS** for production (CloudFront + ACM for frontend, API Gateway for backend)
4. **Regularly update dependencies** to patch security vulnerabilities
5. **Use environment variables** for all sensitive configuration
6. **Enable AWS CloudTrail** for audit logging
7. **Use AWS Secrets Manager** for production secrets instead of environment variables

## Performance Optimization

### Backend
- Use connection pooling for database
- Enable Redis for session storage (optional)
- Configure Lambda reserved concurrency for consistent performance

### Frontend
- Enable gzip compression in CloudFront
- Use lazy loading for Angular modules
- Optimize images and assets
- Configure CloudFront caching policies

## Monitoring and Logging

### Backend
```bash
# View Lambda logs
zappa tail production --since 1h

# CloudWatch Logs
aws logs tail /aws/lambda/your-function-name --follow
```

### Frontend
- CloudFront access logs
- S3 server access logging
- Browser console for client-side errors

## Backup and Recovery

### Database Backup
```bash
# Create backup
pg_dump -h localhost -U postgres awesome_notes > backup.sql

# Restore backup
psql -h localhost -U postgres awesome_notes < backup.sql

# RDS Automated Backups
# Configure in AWS Console → RDS → Automated backups
```

### Application Code
- All code is version controlled in Git
- Use GitHub releases for versioning
- Tag deployments for easy rollback

## Support

For issues or questions:
1. Check this documentation
2. Review GitHub issues
3. Check application logs
4. Contact the development team
