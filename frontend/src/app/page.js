"use client";
import { useEffect, useState } from "react";
import Link from "next/link";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export default function Home() {
  const [message, setMessage] = useState("");
  const [result, setResult] = useState(null);
  const [cart, setCart] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [addedProductId, setAddedProductId] = useState(null);
  useEffect(() => {
    async function loadCart() {
      const response = await fetch(`${API_URL}/cart/1`);
      const data = await response.json();
      setCart(data);
    }

    loadCart();
  }, []);


  async function handleSearch() {
    if (!message.trim()) {
      setError("Please enter a shopping request.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const response = await fetch(
        `${API_URL}/assistant/?user_id=1&message=${encodeURIComponent(message)}`
      );

      if (!response.ok) {
        throw new Error("Request failed");
      }

      const data = await response.json();
      setResult(data);
    } catch (error) {
      setError("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  }
  
  async function handleAddToCart(productId) {
    try {
      const response = await fetch(
        `${API_URL}/cart/add/?user_id=1&product_id=${productId}&quantity=1`,
        {
          method: "POST",
        }
      );

      const data = await response.json();

      if (!response.ok || !data.items) {
        setError(data.message || "Could not add item to cart.");
        return;
      }

      setCart(data);
      setError("");
      setAddedProductId(productId);

      setTimeout(() => {
        setAddedProductId(null);
      }, 2000);
    } catch (error) {
      setError("Could not add item to cart. Please try again.");
    }
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-pink-100 via-white to-blue-100 px-8 py-8 text-slate-900">
      <div className="mx-auto max-w-6xl">
        <div className="mb-10 flex items-center justify-between">
          <div>
            <p className="text-xl font-bold text-slate-900">ShopSense AI</p>
            <p className="text-xs text-slate-500">
              Your intelligent shopping assistant
            </p>
          </div>

          <Link
            href="/cart"
            className="rounded-full border border-violet-200 bg-white/80 px-5 py-2 text-sm font-medium text-violet-700 shadow-sm transition hover:bg-violet-50"
          >
            View Cart{" "}
            {cart && cart.items.length > 0 && `(${cart.items.length})`}
          </Link>
        </div>

        <div className="mb-12 grid items-center gap-10 lg:grid-cols-2">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.25em] text-violet-500">
              AI Shopping Assistant
            </p>

            <h1 className="mt-3 text-5xl font-bold leading-tight text-slate-900">
              Shop smarter with <span className="text-violet-600">natural</span>{" "}
              language
            </h1>

            <p className="mt-4 text-lg text-slate-600">
              Ask for what you need, set your budget or delivery preference, and
              get relevant product recommendations instantly.
            </p>
          </div>

          <div className="relative flex h-80 items-center justify-center">
            <div className="absolute h-72 w-72 rounded-full bg-pink-300/40 blur-3xl" />

            <div className="absolute left-20 top-8 h-64 w-64 rounded-[45%_55%_60%_40%] bg-violet-300/40 blur-2xl" />

            <div className="absolute right-12 bottom-6 h-56 w-56 rounded-[55%_45%_40%_60%] bg-blue-300/40 blur-2xl" />

            <div className="absolute h-72 w-72 rounded-full border border-white/70" />

            <div className="absolute left-1/2 top-[47%] flex w-64 -translate-x-1/2 -translate-y-1/2 items-center gap-3 rounded-full border border-white/70 bg-white/85 px-5 py-4 shadow-xl backdrop-blur-md">
              <span className="text-violet-600">✦</span>
              <span className="text-sm text-slate-600">
                Find wireless earphones under ₹2,000
                <span className="ml-1 inline-block animate-pulse text-violet-600">
                  |
                </span>
              </span>
            </div>
          </div>
        </div>
        <div className="mb-6 flex items-center justify-between">
          <p className="text-sm font-medium text-slate-500">
            Try a natural request like “reorder shampoo and find walking shoes
            under ₹2,000”
          </p>
        </div>

        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSearch();
          }}
          className="flex gap-2"
        >
          <input
            type="text"
            placeholder="What are you looking for?"
            value={message}
            onChange={(e) => {
              setMessage(e.target.value);
              setError("");
            }}
            className="flex-1 rounded-2xl border border-violet-200 bg-white px-5 py-4 text-slate-900 placeholder-slate-400 shadow-sm outline-none transition focus:border-violet-400 focus:ring-4 focus:ring-violet-100"
          />

          <button
            type="submit"
            className="rounded-2xl bg-violet-600 px-6 py-4 font-medium text-white shadow-sm transition hover:bg-violet-500"
          >
            {loading ? "Searching..." : "Search"}
          </button>
        </form>

        {error && <p className="mt-3 text-rose-400">{error}</p>}

        {result?.intent && (
          <div className="mt-5 flex flex-wrap items-center gap-x-7 gap-y-2 border-t border-violet-100 pt-4 text-sm">
            <span className="text-xs font-semibold uppercase tracking-[0.2em] text-violet-500">
              AI Parsed
            </span>

            {result.intent.reorder_product && (
              <span className="text-slate-600">
                Reorder{" "}
                <span className="font-medium text-slate-900">
                  {result.intent.reorder_product}
                </span>
              </span>
            )}

            {result.intent.search_query && (
              <span className="text-slate-600">
                Search{" "}
                <span className="font-medium text-slate-900">
                  {result.intent.search_query}
                </span>
              </span>
            )}

            {result.intent.max_price && (
              <span className="text-slate-600">
                ₹{result.intent.max_price} max
              </span>
            )}
            {result.intent.max_delivery_days && (
              <span className="text-slate-600">
                Delivery ≤ {result.intent.max_delivery_days} days
              </span>
            )}
          </div>
        )}

        {result?.message && (
          <div className="mt-4 inline-flex items-center gap-2 rounded-xl border border-violet-100 bg-white/70 px-4 py-3 text-sm text-slate-600 shadow-sm">
            <span className="text-violet-500">ⓘ</span>
            <span>{result.message}</span>
          </div>
        )}

        {result?.reorder && (
          <div className="mt-10 rounded-3xl bg-white/90 p-8 shadow-xl backdrop-blur">
            <p className="text-sm font-semibold uppercase tracking-wide text-violet-500">
              Matched from your purchase history
            </p>

            <h2 className="mt-2 text-2xl font-semibold text-slate-900">
              {result.reorder.product_name}
            </h2>

            <p className="mt-2 text-2xl font-bold text-violet-700">
              ₹{result.reorder.price}
            </p>

            <p className="mt-2 text-sm text-slate-500">
              Previous quantity: {result.reorder.quantity}
            </p>
            <p className="mt-3 text-sm text-slate-500">
              Reorder matched from your previous purchase.
            </p>
          </div>
        )}

        {result?.discovery && (
          <div className="mt-10 w-full rounded-3xl bg-white/90 p-8 shadow-xl backdrop-blur">
            <h2 className="mb-5 text-xl font-semibold text-slate-900">
              Recommendations
            </h2>
            <p className="mb-6 text-sm text-slate-500">
              Selected based on your request and shopping preferences.
            </p>

            {result.discovery.length === 0 ? (
              <p className="text-slate-500">No matching products found.</p>
            ) : (
              <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-3">
                {result.discovery.map((product) => (
                  <div
                    key={product.id}
                    className="rounded-2xl border border-violet-100 bg-white p-5 shadow-sm transition hover:-translate-y-1 hover:shadow-md"
                  >
                    <p className="mb-3 text-xs font-semibold uppercase tracking-wide text-violet-500">
                      AI Pick
                    </p>

                    <h3 className="text-lg font-semibold text-slate-900">
                      {product.name}
                    </h3>

                    <p className="mt-2 text-2xl font-bold text-violet-700">
                      ₹{product.price}
                    </p>

                    <p className="mt-2 text-sm text-slate-500">
                      {product.category}
                    </p>

                    <p className="mt-1 text-sm text-slate-500">
                      Delivery: {product.delivery_days}{" "}
                      {product.delivery_days === 1 ? "day" : "days"}
                    </p>

                    <button
                      onClick={() => handleAddToCart(product.id)}
                      className="mt-5 w-full rounded-xl bg-violet-600 px-4 py-3 text-white transition hover:bg-violet-500"
                    >
                      Add to Cart
                    </button>
                    {addedProductId === product.id && (
                      <div className="mt-3 inline-flex items-center gap-2 rounded-full bg-violet-50 px-3 py-1.5 text-xs font-medium text-violet-700">
                        <span>✓</span>
                        <span>Added to cart</span>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </main>
  );
}
