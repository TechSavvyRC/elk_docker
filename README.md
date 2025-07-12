# Banking Transaction Monitoring System

A comprehensive real-time banking transaction monitoring system built with Docker, featuring the ELK Stack (Elasticsearch, Logstash, Kibana) and Apache Kafka for high-performance data ingestion and visualization.

## 🏗️ Architecture Overview

```ascii
┌────────────────────────────────────────────────────────────────────────────────┐
│                      Banking Transaction Monitoring System                     │
├────────────────────────────────────────────────────────────────────────────────┤
│                                                                                │
│  ┌─────────────────┐    ┌─────────────────┐    ┌────────────────────────────┐  │
│  │  Banking App    │────│  Apache Kafka   │────│        Logstash            │  │
│  │  (Python)       │    │  (Message Bus)  │    │   (Data Processing)        │  │
│  │                 │    │                 │    │                            │  │
│  │ • Generates     │    │ • Topic: banking│    │ • Transforms data          │  │
│  │   transactions  │    │ • Port: 9092    │    │ • Enriches logs            │  │
│  │ • Kafka producer│    │                 │    │ • Forwards to ES           │  │
│  └─────────────────┘    └─────────────────┘    └────────────────────────────┘  │
│                                  │                           │                 │
│                                  │                           │                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌────────────────────────────┐  │
│  │   Zookeeper     │    │                 │    │                            │  │
│  │ (Kafka Manager) │    │                 │    │                            │  │
│  │                 │    │                 │    │                            │  │
│  │ • Port: 2181    │    │                 │    │                            │  │
│  │ • Cluster coord │    │                 │    │                            │  │
│  └─────────────────┘    │                 │    │                            │  │
│                         │  Elasticsearch  │    │           Kibana           │  │
│                         │     Cluster     │────│       (2 Instances)        │  │
│                         │                 │    │                            │  │
│                         │ ┌─────────────┐ │    │ • kibana-01: Port 5601     │  │
│                         │ │ Coordinator │ │    │ • kibana-02: Port 5602     │  │
│                         │ │Port: 9200   │ │    │ • SSL enabled              │  │
│                         │ └─────────────┘ │    │ • Load balanced            │  │
│                         │                 │    │                            │  │
│                         │ ┌─────────────┐ │    └────────────────────────────┘  │
│                         │ │Master Node-1│ │                                    │
│                         │ │Port: 9201   │ │                                    │
│                         │ └─────────────┘ │                                    │
│                         │                 │                                    │
│                         │ ┌─────────────┐ │                                    │
│                         │ │Master Node-2│ │                                    │
│                         │ │Port: 9202   │ │                                    │
│                         │ └─────────────┘ │                                    │
│                         │                 │                                    │
│                         │ ┌─────────────┐ │                                    │
│                         │ │Master Node-3│ │                                    │
│                         │ │Port: 9203   │ │                                    │
│                         │ └─────────────┘ │                                    │
│                         └─────────────────┘                                    │
│                                                                                │
└────────────────────────────────────────────────────────────────────────────────┘

Networks:
├── elastic_network (Elasticsearch, Kibana, Logstash)
└── kafka_network (Kafka, Zookeeper, Banking App)
```

## 🚀 Features

### Core Functionality
- **Real-time Transaction Processing**: Simulates banking transactions with realistic data patterns
- **High Availability**: Multi-node Elasticsearch cluster with dedicated coordinator
- **Scalable Architecture**: Containerized microservices for easy scaling
- **Security First**: End-to-end SSL/TLS encryption across all services
- **Data Visualization**: Dual Kibana instances for load balancing and redundancy

### Technical Highlights
- **Elasticsearch Cluster**: 4-node setup (1 coordinator + 3 master/data nodes)
- **Kafka Integration**: Reliable message streaming with Zookeeper coordination
- **Custom Banking App**: Python-based transaction generator
- **SSL Security**: Automatic certificate generation and management
- **Health Monitoring**: Comprehensive health checks for all services
- **Data Persistence**: Volume-based storage for data durability

## 📋 Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- At least 8GB RAM available for containers
- 10GB free disk space

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd banking-transaction-monitoring
```

### 2. Create Environment File
Create a `.env` file in the project root:

```env
# Elasticsearch Configuration
STACK_VERSION=8.8.0
CLUSTER_NAME=banking-cluster
LICENSE=basic
ES_PORT=9200
ES_USER=elastic
ES_PASSWORD=your_secure_password_here
ES_MEM_LIMIT=1073741824

# Kibana Configuration
KIBANA_PORT=5601
KIBANA_USER=kibana_system
KIBANA_PASSWORD=your_kibana_password_here
KB_MEM_LIMIT=1073741824

# Kafka Configuration
KAFKA_PORT=9092
KAFKA_BOOTSTRAP_SERVERS=kafka:9092
KAFKA_TOPIC_1=banking_transactions
ZK_PORT=2181
```

### 3. Project Structure Setup
Ensure your project structure looks like this:

```
banking-transaction-monitoring/
├── docker-compose.yml
├── .env
├── banking/
│   ├── Dockerfile
│   ├── banking_app.py
│   └── requirements.txt
├── logstash/
│   ├── Dockerfile
│   └── pipeline/
│       └── logstash.conf
└── README.md
```

### 4. Build and Start Services
```bash
# Start all services
docker-compose up -d

# Monitor startup logs
docker-compose logs -f setup

# Check service status
docker-compose ps
```

## 🔧 Service Details

### Elasticsearch Cluster
- **Coordinator Node**: `es-coord` (Port 9200) - Handles client requests
- **Master Node 1**: `es-masternode-01` (Port 9201) - Cluster management + data
- **Master Node 2**: `es-masternode-02` (Port 9202) - Cluster management + data  
- **Master Node 3**: `es-masternode-03` (Port 9203) - Cluster management + data

### Kibana Instances
- **Primary**: `kibana-01` (Port 5601) - Main dashboard interface
- **Secondary**: `kibana-02` (Port 5602) - Load balancing/redundancy

### Kafka Ecosystem
- **Zookeeper**: Port 2181 - Kafka cluster coordination
- **Kafka Broker**: Port 9092 - Message streaming platform

### Custom Applications
- **Banking App**: Transaction generator and Kafka producer
- **Logstash**: Data processing pipeline

## 🌐 Access Points

| Service | URL | Credentials |
|---------|-----|-------------|
| Kibana Primary | https://localhost:5601 | elastic / [ES_PASSWORD] |
| Kibana Secondary | https://localhost:5602 | elastic / [ES_PASSWORD] |
| Elasticsearch | https://localhost:9200 | elastic / [ES_PASSWORD] |

## 📊 Monitoring & Management

### Health Checks
```bash
# Check all services
docker-compose ps

# View specific service logs
docker-compose logs -f banking-app
docker-compose logs -f logstash
docker-compose logs -f es-coord

# Check Elasticsearch cluster health
curl -k -u elastic:your_password https://localhost:9200/_cluster/health
```

### Kafka Management
```bash
# List topics
docker exec -it marvel-kafka kafka-topics --list --bootstrap-server localhost:9092

# Monitor banking transactions topic
docker exec -it marvel-kafka kafka-console-consumer --topic banking_transactions --bootstrap-server localhost:9092
```

## 🔒 Security Features

### SSL/TLS Configuration
- **Automatic Certificate Generation**: Setup service creates CA and node certificates
- **End-to-end Encryption**: All inter-service communication secured
- **Certificate Management**: Centralized certificate storage and distribution

### Authentication
- **Elasticsearch Security**: Built-in user authentication with role-based access
- **Kibana Integration**: Secure connection to Elasticsearch cluster
- **Service Isolation**: Network segmentation between service groups

## 📈 Performance Tuning

### Memory Configuration
```yaml
# Elasticsearch nodes
ES_JAVA_OPTS: -Xms512m -Xmx512m

# Logstash
LS_JAVA_OPTS: -Xmx1g -Xms1g
```

### Scaling Options
- **Horizontal Scaling**: Add more Elasticsearch data nodes
- **Kafka Partitioning**: Increase topic partitions for higher throughput
- **Kibana Load Balancing**: Add nginx proxy for Kibana instances

## 🛡️ Troubleshooting

### Common Issues

**1. Certificate Errors**
```bash
# Restart setup service to regenerate certificates
docker-compose restart setup
```

**2. Memory Issues**
```bash
# Increase Docker memory limit
# Check container resource usage
docker stats
```

**3. Service Dependencies**
```bash
# Restart services in order
docker-compose stop
docker-compose up -d
```

**4. Elasticsearch Yellow/Red Status**
```bash
# Check cluster allocation
curl -k -u elastic:password https://localhost:9200/_cluster/allocation/explain
```

### Log Locations
- **Elasticsearch**: `docker-compose logs es-coord`
- **Kibana**: `docker-compose logs kibana-01`
- **Kafka**: `docker-compose logs kafka`
- **Banking App**: `docker-compose logs banking-app`

## 📝 Development

### Adding New Features
1. **New Kafka Topics**: Update environment variables and logstash configuration
2. **Custom Dashboards**: Import via Kibana UI or API
3. **Data Enrichment**: Modify logstash pipeline configuration
4. **Banking Logic**: Update banking_app.py for new transaction types

### Testing
```bash
# Test Kafka connectivity
docker exec -it marvel-kafka kafka-topics --list --bootstrap-server localhost:9092

# Test Elasticsearch
curl -k -u elastic:password https://localhost:9200/_cat/indices

# Test banking app
docker-compose logs banking-app
```

## 📚 Additional Resources

- [Elasticsearch Documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
- [Kibana User Guide](https://www.elastic.co/guide/en/kibana/current/index.html)
- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [Docker Compose Reference](https://docs.docker.com/compose/)
