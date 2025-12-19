# Deployment Instructions

This document provides various deployment options for the Integrated RAG Chatbot depending on your environment and requirements.

## Local Development Deployment

For local development and testing:

### Prerequisites
- Python 3.11+
- Git
- Access to Cohere API (with provided API key)
- Access to Qdrant Cloud (with provided URL and API key)
- Access to Neon Serverless Postgres (with provided connection URL)

### Steps
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   Copy `.env.example` to `.env` and update with your actual API keys and connection strings:
   ```bash
   cp .env.example .env
   # Edit .env to add your actual credentials
   ```

5. Run the application:
   ```bash
   cd backend_backup
   uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
   ```

The API will be available at `http://localhost:8000`.

## Docker Deployment

### Prerequisites
- Docker and Docker Compose

### Steps
1. Create a `Dockerfile`:
   ```Dockerfile
   FROM python:3.11-slim

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   EXPOSE 8000

   CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

2. Create a `docker-compose.yml`:
   ```yaml
   version: '3.8'

   services:
     rag-chatbot:
       build: .
       ports:
         - "8000:8000"
       environment:
         - COHERE_API_KEY=${COHERE_API_KEY}
         - QDRANT_URL=${QDRANT_URL}
         - QDRANT_API_KEY=${QDRANT_API_KEY}
         - NEON_DB_URL=${NEON_DB_URL}
         - API_KEY=${API_KEY}
       volumes:
         - ./data:/app/data
   ```

3. Set your environment variables in a `.env` file in the same directory as your `docker-compose.yml`

4. Build and run:
   ```bash
   docker-compose up --build
   ```

## Cloud Deployment Options

### Deploy to Heroku

#### Prerequisites
- Heroku CLI installed
- Heroku account

#### Steps
1. Login to Heroku:
   ```bash
   heroku login
   ```

2. Create a new Heroku app:
   ```bash
   heroku create your-app-name
   ```

3. Set environment variables:
   ```bash
   heroku config:set COHERE_API_KEY="your-cohere-api-key" \
                   QDRANT_URL="your-qdrant-url" \
                   QDRANT_API_KEY="your-qdrant-api-key" \
                   NEON_DB_URL="your-neon-db-url" \
                   API_KEY="your-secret-api-key"
   ```

4. Deploy the application:
   ```bash
   git push heroku main
   ```

### Deploy to AWS (Elastic Beanstalk)

#### Prerequisites
- AWS account
- EB CLI installed

#### Steps
1. Initialize Elastic Beanstalk:
   ```bash
   eb init
   ```

2. Create a new environment:
   ```bash
   eb create rag-env
   ```

3. Set environment variables:
   ```bash
   eb setenv COHERE_API_KEY="your-cohere-api-key" \
             QDRANT_URL="your-qdrant-url" \
             QDRANT_API_KEY="your-qdrant-api-key" \
             NEON_DB_URL="your-neon-db-url" \
             API_KEY="your-secret-api-key"
   ```

4. Deploy the application:
   ```bash
   eb deploy
   ```

### Deploy to Google Cloud Run

#### Prerequisites
- Google Cloud account with Cloud Run API enabled
- gcloud CLI installed

#### Steps
1. Build and push the Docker image:
   ```bash
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/rag-chatbot
   ```

2. Deploy to Cloud Run:
   ```bash
   gcloud run deploy --image gcr.io/YOUR_PROJECT_ID/rag-chatbot \
     --platform managed \
     --region YOUR_REGION \
     --set-env-vars COHERE_API_KEY="your-cohere-api-key",QDRANT_URL="your-qdrant-url",QDRANT_API_KEY="your-qdrant-api-key",NEON_DB_URL="your-neon-db-url",API_KEY="your-secret-api-key" \
     --port 8000 \
     --allow-unauthenticated
   ```

## Kubernetes Deployment

### Prerequisites
- Kubernetes cluster
- kubectl configured to connect to the cluster
- Docker image pushed to a registry

### Steps

1. Create a namespace for the application:
   ```bash
   kubectl create namespace rag-chatbot
   ```

2. Create a Secret for environment variables:
   ```bash
   kubectl create secret generic rag-secrets \
     --namespace rag-chatbot \
     --from-literal=COHERE_API_KEY="your-cohere-api-key" \
     --from-literal=QDRANT_URL="your-qdrant-url" \
     --from-literal=QDRANT_API_KEY="your-qdrant-api-key" \
     --from-literal=NEON_DB_URL="your-neon-db-url" \
     --from-literal=API_KEY="your-secret-api-key"
   ```

3. Create a `deployment.yaml`:
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: rag-chatbot
     namespace: rag-chatbot
   spec:
     replicas: 1
     selector:
       matchLabels:
         app: rag-chatbot
     template:
       metadata:
         labels:
           app: rag-chatbot
       spec:
         containers:
         - name: rag-chatbot
           image: YOUR_REGISTRY/rag-chatbot:latest
           ports:
           - containerPort: 8000
           envFrom:
           - secretRef:
               name: rag-secrets
         restartPolicy: Always
   ---
   apiVersion: v1
   kind: Service
   metadata:
     name: rag-chatbot-service
     namespace: rag-chatbot
   spec:
     selector:
       app: rag-chatbot
     ports:
     - protocol: TCP
       port: 80
       targetPort: 8000
     type: LoadBalancer
   ```

4. Apply the deployment:
   ```bash
   kubectl apply -f deployment.yaml
   ```

## Production Considerations

### Security
- Use HTTPS in production
- Regularly rotate API keys
- Implement proper authentication and authorization
- Regular security audits

### Monitoring & Logging
- Set up proper logging (structured JSON logs)
- Monitor API response times and error rates
- Track usage metrics to ensure staying within service limits
- Set up alerts for high-error rates or slow response times

### Performance Optimization
- Use a CDN for static assets
- Implement caching for frequent queries
- Optimize database queries
- Use load balancers for high-traffic deployments

### Scaling
- Consider horizontal pod autoscaling in Kubernetes
- Implement distributed processing for large batch operations
- Use connection pooling for database connections
- Consider implementing Redis for caching

### Resource Limits
- Monitor and set appropriate CPU and memory limits
- Implement graceful degradation when resources are tight
- Use resource quotas in multi-tenant environments