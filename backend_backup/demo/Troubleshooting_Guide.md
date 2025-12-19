# Troubleshooting Guide for Integrated RAG Chatbot

## Common Issues and Solutions

### Authentication Issues

**Issue**: "401 Unauthorized" error when making API requests
- **Cause**: Missing or incorrect API key
- **Solution**: 
  1. Verify your API key is correctly set in your `.env` file as `API_KEY=your_secret_api_key_here`
  2. Ensure your requests include the header `Authorization: Bearer your_secret_api_key_here`
  3. Check that the API key in your request matches the one in your environment file

**Issue**: "Invalid API key" error
- **Cause**: The API key format might be incorrect
- **Solution**: Make sure your API key is a strong, random string; regenerate it if necessary

### Ingestion Issues

**Issue**: File upload fails with "Invalid file format" error
- **Cause**: The file format is not supported
- **Solution**: Ensure you're uploading a PDF, HTML, or TXT file. Check your file extension is one of: `.pdf`, `.html`, `.htm`, `.txt`

**Issue**: "File size exceeds limit" error
- **Cause**: The uploaded file is too large
- **Solution**: By default, the system only accepts files under 50MB. You can adjust this limit in your settings file by changing the `max_file_size` parameter.

**Issue**: Book status stays in PROCESSING for a long time
- **Cause**: The book is large or the system is busy
- **Solution**: 
  1. Check the monitoring endpoint for resource usage
  2. Review the application logs for any errors
  3. Large books may take several minutes to process

### Query Issues

**Issue**: "Book ID not found" error
- **Cause**: The book ID doesn't exist in the database or hasn't been processed yet
- **Solution**: 
  1. Verify the book ID is correct
  2. Check the status of your book using the `/ingest/status/{book_id}` endpoint
  3. Ensure the book has reached "READY" status before querying

**Issue**: Query returns irrelevant results
- **Cause**: The vector embeddings or search parameters might need tuning
- **Solution**: 
  1. Verify the embedding model is working correctly
  2. Increase the `max_results` parameter to retrieve more context
  3. Experiment with different values for the `temperature` parameter

**Issue**: Slow query response times (>2 seconds)
- **Cause**: Database queries may be inefficient or system resources may be low
- **Solution**: 
  1. Check your vector database indexes
  2. Verify that your Cohere API is responding quickly
  3. Monitor system resource usage

### External Service Issues

**Issue**: "Failed to connect to Cohere" error
- **Cause**: Incorrect API key or network connectivity issue
- **Solution**: 
  1. Verify your Cohere API key is set correctly in your `.env` file
  2. Test your connection to the Cohere API directly
  3. Check the Cohere status page for any service outages

**Issue**: "Qdrant connection failed" error
- **Cause**: Incorrect URL, API key, or network connectivity issue
- **Solution**: 
  1. Verify your Qdrant URL and API key in your `.env` file
  2. Ensure your Qdrant Cloud instance is running
  3. Check firewall rules if running in a corporate environment

**Issue**: "PostgreSQL connection failed" error
- **Cause**: Incorrect database URL or network connectivity issue
- **Solution**: 
  1. Verify your Neon Postgres connection string in your `.env` file
  2. Check that your Neon database is provisioned and running
  3. Confirm SSL settings in your connection string

### Monitoring and Usage Issues

**Issue**: Usage metrics not updating or showing incorrect values
- **Cause**: The monitoring script may not be tracking usage correctly
- **Solution**: 
  1. Run the monitoring script manually: `python scripts/monitor_usage.py`
  2. Check the application logs for any errors
  3. Verify that your external service credentials are correct and have read access

**Issue**: Receiving alerts about approaching limits
- **Cause**: You may be nearing the limits of your free-tier services
- **Solution**: 
  1. Review the usage metrics to identify which service is approaching its limit
  2. Optimize your usage by reducing query frequency, chunk size, or data retention
  3. Consider upgrading to paid tier if needed

## Performance Issues

### High Memory Usage

**Symptoms**: Application running slowly or crashing
**Possible Causes**:
- Processing large files simultaneously
- Caching too much data in memory
- Memory leaks in the application

**Solutions**:
1. Process files in smaller batches
2. Implement proper garbage collection
3. Monitor memory usage during processing
4. Consider using generators instead of loading all data into memory

### Slow Response Times

**Symptoms**: Queries taking more than 2 seconds
**Possible Causes**:
- Large chunks to embed or generate
- Network latency to external services
- Database query inefficiencies

**Solutions**:
1. Reduce the number of results retrieved per query
2. Optimize database indexes
3. Implement caching for frequent queries
4. Check external service response times

## Debugging Tips

### Enable Verbose Logging

To get more detailed information about what's happening in your application:

1. Set the `LOG_LEVEL` environment variable to "DEBUG" in your `.env` file:
   ```
   LOG_LEVEL=DEBUG
   ```

2. Restart your application to apply the new logging level.

### Analyze Application Logs

Application logs can be found in the `logs/` directory. Look for:
- Error timestamps that correspond to when you noticed the issue
- Specific error messages and stack traces
- Resource usage information
- External service call durations

### Test Individual Components

To isolate issues:

1. Test your Cohere integration directly:
   ```python
   import cohere
   client = cohere.Client("YOUR_API_KEY")
   response = client.embed(texts=["test"], model="embed-english-v3.0")
   ```

2. Test your Qdrant connection:
   ```python
   from qdrant_client import QdrantClient
   client = QdrantClient(url="YOUR_QDRANT_URL", api_key="YOUR_QDRANT_API_KEY")
   client.get_collections()
   ```

3. Test your database connection:
   ```python
   import psycopg2
   conn = psycopg2.connect("YOUR_NEON_DB_URL")
   conn.close()
   ```

## When to Seek Help

Contact your development team or service providers if you encounter:
- Persistent issues with external service connections despite verifying credentials
- Consistent errors that don't match any troubleshooting steps
- Performance issues that significantly impact user experience
- Security concerns or suspected breaches

## Preventive Measures

1. Regularly monitor usage metrics to anticipate approaching limits
2. Implement proper error handling and logging in your application
3. Set up alerts for critical system metrics
4. Maintain up-to-date backups of your data
5. Regularly test your system with realistic loads
6. Keep your dependencies updated to the latest stable versions