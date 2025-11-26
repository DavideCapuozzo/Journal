# Journal - Blockchain-Enabled Blog Platform

A Django-based blog application that integrates Ethereum blockchain technology to create immutable records of blog posts. Each post is registered on the Ethereum Sepolia testnet, ensuring transparency and verifiability.

## Features

- **User Authentication**: Registration, login, and logout functionality
- **Blockchain Integration**: Each post is recorded on Ethereum Sepolia testnet with a unique transaction ID
- **Redis Integration**: IP tracking for admin users to monitor login locations
- **Responsive Design**: Bootstrap-based UI with clean blog theme

## Technology Stack

- **Backend**: Django 5.2.8
- **Database**: SQLite3
- **Blockchain**: Web3.py with Ethereum Sepolia testnet
- **Cache/Session**: Redis
- **Frontend**: Bootstrap 5, HTML, CSS, JavaScript
- **Forms**: Django Crispy Forms with Bootstrap 5

## Installation

### Prerequisites

- Python 3.13+
- Redis server
- Ethereum Sepolia testnet ETH (for blockchain transactions)

### Setup

1. **Clone the repository**
   ```bash
   cd Journal
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install django web3 redis crispy-bootstrap5 python-dotenv
   ```

4. **Configure Redis**
   - Install and start Redis server on localhost:6379
   - Or update Redis settings in `.env` file

5. **Get Sepolia testnet ETH**
   - Visit [Alchemy Sepolia Faucet](https://www.alchemy.com/faucets/ethereum-sepolia)
   - Request test ETH for your wallet address
   - Ensure wallet has at least 0.05 ETH for transactions

6. **Run migrations**
   ```bash
   cd Journal
   python manage.py migrate
   ```

7. **Access the application**
    - Open browser: `http://127.0.0.1:8000`

## Project Structure

```
Journal/
├── app/
│   ├── models.py          # Post model with blockchain fields
│   ├── views.py           # Main application logic
│   ├── forms.py           # User registration and post forms
│   ├── urls.py            # URL routing
│   ├── templates/
│   │   └── app/
│   │       ├── index.html         # Homepage with post list
│   │       ├── blog_post.html     # Create post page
│   │       ├── post_details.html  # Individual post view
│   │       ├── login.html         # Login page
│   │       ├── register.html      # Registration page
│   │       └── search_post.html   # Search page
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── img/
│   └── migrations/
├── Journal/
│   ├── settings.py        # Django settings
│   ├── urls.py            # Root URL configuration
│   └── wsgi.py
├── manage.py
└── db.sqlite3
```

## Key Features Explained

### Blockchain Integration

When a blog post is created:
1. Post data is serialized and hashed using SHA-256
2. A transaction is created on Ethereum Sepolia testnet
3. Transaction hash (`txId`) and unique identifier are stored with the post
4. If blockchain transaction fails (insufficient funds), post is saved without blockchain data

### Post Model Fields

- `author`: Foreign key to User model
- `title`: Post title (max 200 chars)
- `subtitle`: Optional subtitle (max 150 chars)
- `text`: Post content (TextField)
- `created_date`: Auto-generated timestamp
- `published_date`: Optional publication date
- `identifier`: 10-character unique alphanumeric code
- `txId`: Ethereum transaction hash (66 chars)

## API Endpoints

- `/` - Homepage with all posts
- `/register` - User registration
- `/login` - User login
- `/logout` - User logout
- `/blogpost` - Create new post (authenticated users only)
- `/post` - Alternative route to create post
- `/post_details/<id>` - View specific post
- `/search_post` - Search posts by identifier
- `/admin` - Django admin panel

## Configuration

All configuration is managed through environment variables in the `.env` file located in the project root directory.

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Django Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Database
DATABASE_ENGINE=django.db.backends.sqlite3
DATABASE_NAME=db.sqlite3

# Ethereum Blockchain
INFURA_API_KEY=your-infura-api-key
ETH_NETWORK_URL=https://sepolia.infura.io/v3/your-infura-api-key
ETH_PRIVATE_KEY=your-ethereum-private-key
ETH_ADDRESS=your-ethereum-address
GAS_LIMIT=21000

# Redis
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_DB=0

# Application Settings
LANGUAGE_CODE=en-us
TIME_ZONE=UTC
CRISPY_TEMPLATE_PACK=bootstrap5
```

## Create a Wallet
```
python -c "from eth_account import Account; account = Account.create(); print(f'Address: {account.address}'); print(f'Private Key: {account.key.hex()}')"
```

## Getting Testnet ETH

To enable blockchain features, obtain Sepolia testnet ETH:
1. Visit [Alchemy Sepolia Faucet](https://www.alchemy.com/faucets/ethereum-sepolia)
2. Connect wallet or enter address
3. Request test ETH (0.05-0.5 ETH)
4. Wait for transaction confirmation

## Troubleshooting

### Blockchain Transaction Fails
- **Issue**: `insufficient funds for gas`
- **Solution**: Add Sepolia testnet ETH to your wallet address

### Redis Connection Error
- **Issue**: `Error connecting to Redis`
- **Solution**: Ensure Redis server is running on the configured port

### Form Validation Errors
- **Issue**: Post not saving
- **Solution**: Check all required fields (title, text) are filled

## Acknowledgments

- Django framework
- Web3.py library
- Bootstrap Clean Blog theme
- Infura for Ethereum node access
- Redis for caching
