# ShopSense AI

ShopSense AI is an end-to-end natural-language shopping assistant that helps users discover products, reorder previous purchases, and manage shopping requests through a single interface.


## Why ShopSense AI?

Online shopping can become repetitive and time-consuming when users need to manually search for products, apply multiple filters, compare alternatives, and revisit previous purchases to reorder items.

ShopSense AI simplifies this process through a single natural-language interface where users can express complete shopping requests, including product discovery, budget constraints, delivery preferences, exclusions, and reorders.

The system interprets the user's intent, retrieves relevant products, applies constraints, and ranks results using semantic similarity, reducing the number of manual steps required to reach a suitable product.


## Features

- Natural-language product discovery
- Reorder products from purchase history
- Handle mixed shopping queries
- Filter products by budget, stock, exclusions, and delivery time
- Semantic product search using embeddings and cosine similarity
- Persistent shopping cart with quantity updates and item removal


## Tech Stack

### Frontend
- Next.js
- Tailwind CSS

### Backend
- FastAPI
- SQLAlchemy

### AI
- Groq API for intent extraction
- Gemini Embeddings API
- Cosine similarity for semantic search

### Database
- PostgreSQL
- Supabase

### Deployment
- Vercel


## How It Works

1. The user enters a natural-language shopping request.
2. Groq extracts structured intent such as:
   - request type
   - product query
   - budget
   - delivery constraint
   - exclusions
3. Purchase history is checked for reorder requests.
4. The user query is converted into an embedding using Gemini.
5. The query embedding is compared with stored product embeddings using cosine similarity.
6. Product constraints are applied.
7. The most relevant products are returned to the user.
8. Products can be added to a persistent shopping cart.


## Architecture

```text
User
  |
  v
Next.js Frontend
  |
  v
FastAPI Backend
  |
  +--> Groq API
  |      |
  |      +--> Intent Extraction
  |
  +--> Gemini Embeddings
  |      |
  |      +--> Query Embedding
  |
  +--> Supabase PostgreSQL
         |
         +--> Products
         +--> Purchase History
         +--> Cart
         +--> Stored Product Embeddings

FastAPI Backend
  |
  +--> Query Embedding
  +--> Stored Product Embeddings
           |
           v
     Cosine Similarity
           |
           v
   Ranked Product Results
```

## Live Demo

Try ShopSense AI here:

https://shopsense-ai-gse1.vercel.app


## Example Queries

```text
find walking shoes under 2000
```

```text
reorder shampoo
```

```text
reorder shampoo and find walking shoes under 2000 delivered within 2 days
```


## Key Engineering Decisions

- Migrated from SQLite to PostgreSQL for persistent cloud storage.
- Replaced local Sentence Transformers with Gemini Embeddings to reduce deployment size and memory usage.
- Precomputed and stored product embeddings to reduce repeated computation and API usage.
- Deployed the Next.js frontend and FastAPI backend together on Vercel using a multi-service setup.


## Limitations

- The current product catalogue is limited and primarily used for demonstration.
- Product embeddings need to be regenerated when product information changes.
- The system does not currently support user authentication or multiple user accounts.
- Semantic search uses cosine similarity over stored embeddings rather than a dedicated vector database.
- Checkout and payment processing are outside the current project scope.


## Future Improvements

- Add user authentication and support for multiple user accounts.
- Use a vector database for more scalable semantic search.
- Automatically regenerate embeddings when product data changes.
- Add personalized recommendations based on user history.
- Integrate checkout and payment functionality.