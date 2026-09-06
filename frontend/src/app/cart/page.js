"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export default function CartPage() {
  const [cart, setCart] = useState(null);
  const [cartError, setCartError] = useState({
    productId: null,
    message: "",
  });

  useEffect(() => {
    async function loadCart() {
      const response = await fetch(`${API_URL}/cart/1`);
      const data = await response.json();
      setCart(data);
    }

    loadCart();
  }, []);

  async function handleUpdateQuantity(productId, newQuantity) {
    if (newQuantity <= 0) return;

    try {
      const response = await fetch(
        `${API_URL}/cart/update/?user_id=1&product_id=${productId}&quantity=${newQuantity}`,
        {
          method: "PUT",
        }
      );

      const data = await response.json();

      if (!response.ok || !data.items) {
        setCartError({
          productId: productId,
          message: data.message || "Could not update quantity.",
        });
        return;
      }

      setCart(data);
      setCartError({
        productId: null,
        message: "",
      });
    } catch (error) {
      setCartError({
        productId: productId,
        message: "Could not update quantity. Please try again.",
      });
    }
  }

  async function handleRemoveFromCart(productId) {
    try {
      const response = await fetch(
        `${API_URL}/cart/remove/?user_id=1&product_id=${productId}`,
        {
          method: "DELETE",
        }
      );

      const data = await response.json();

      if (!response.ok || !data.items) {
        setCartError({
          productId: productId,
          message: data.message || "Could not remove item.",
        });
        return;
      }

      setCart(data);

      setCartError({
        productId: null,
        message: "",
      });
    } catch (error) {
      setCartError({
        productId: productId,
        message: "Could not remove item. Please try again.",
      });
    }
  }

  async function handleClearCart() {
    try {
      const response = await fetch(`${API_URL}/cart/clear/1`, {
        method: "DELETE",
      });

      const data = await response.json();

      if (!response.ok || !data.items) {
        setCartError({
          productId: null,
          message: data.message || "Could not clear cart.",
        });
        return;
      }

      setCart(data);

      setCartError({
        productId: null,
        message: "",
      });
    } catch (error) {
      setCartError({
        productId: null,
        message: "Could not clear cart. Please try again.",
      });
    }
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-pink-100 via-white to-blue-100 px-8 py-8 text-slate-900">
      <div className="mx-auto max-w-6xl">
        <Link
          href="/"
          className="inline-flex items-center gap-2 text-sm font-medium text-slate-600 transition hover:text-violet-600"
        >
          ← Back to Assistant
        </Link>

        <div className="mt-6 mb-8">
          <p className="text-sm font-semibold uppercase tracking-[0.25em] text-violet-500">
            Your Cart
          </p>

          <h1 className="mt-2 text-4xl font-bold">Ready to check out?</h1>

          <p className="mt-3 text-slate-600">
            Review your selected items and adjust quantities before continuing.
          </p>
        </div>

        <div className="mt-8 rounded-3xl bg-white/90 p-8 shadow-xl backdrop-blur">
          {cartError.productId === null && cartError.message && (
            <div className="mb-4 inline-flex items-center gap-2 rounded-xl border border-rose-100 bg-white/70 px-4 py-3 text-sm text-rose-500 shadow-sm">
              <span>ⓘ</span>
              <span>{cartError.message}</span>
            </div>
          )}

          {cart && (
            <>
              {cart.items.length === 0 ? (
                <div className="py-16 text-center">
                  <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-violet-100 text-2xl">
                    🛍️
                  </div>

                  <h2 className="text-xl font-semibold text-slate-900">
                    Your cart is empty
                  </h2>

                  <p className="mt-2 text-sm text-slate-500">
                    Ask the assistant to find something for you.
                  </p>

                  <Link
                    href="/"
                    className="mt-6 inline-block rounded-xl bg-violet-600 px-5 py-3 text-white transition hover:bg-violet-500"
                  >
                    Back to Assistant
                  </Link>
                </div>
              ) : (
                <>
                  {cart.items.map((item) => (
                    <div
                      key={item.product_id}
                      className="grid grid-cols-[1.6fr_0.7fr_0.8fr_auto] items-center gap-6 border-b border-slate-200 py-6"
                    >
                      <h3 className="font-semibold">{item.product_name}</h3>

                      <p className="text-slate-900">₹{item.price}</p>

                      <div className="relative justify-self-end">
                      <div className="flex items-center gap-8">
                        <div className="flex items-center gap-2 rounded-full bg-violet-50 px-3 py-2">
                          <button
                            onClick={() =>
                              handleUpdateQuantity(
                                item.product_id,
                                item.quantity - 1
                              )
                            }
                            className="h-8 w-8 rounded-full text-violet-700 transition hover:bg-violet-100"
                          >
                            -
                          </button>

                          <span className="min-w-6 text-center font-medium">
                            {item.quantity}
                          </span>

                          <button
                            onClick={() =>
                              handleUpdateQuantity(
                                item.product_id,
                                item.quantity + 1
                              )
                            }
                            className="h-8 w-8 rounded-full text-violet-700 transition hover:bg-violet-100"
                          >
                            +
                          </button>
                        </div>

                        <button
                          onClick={() => handleRemoveFromCart(item.product_id)}
                          className="text-sm font-medium text-rose-500 transition hover:text-rose-600"
                        >
                          Remove
                        </button>
                      </div>
                      {cartError.productId === item.product_id && (
                        <p className="absolute right-0 mt-1 w-56 pb-2 text-center text-xs font-medium text-rose-500">
                          {cartError.message}
                        </p>
                      )}
                    </div>
                    </div>
                  ))}
                  <div className="mt-6 flex items-center justify-between rounded-2xl bg-violet-50 px-6 py-5">
                    <div>
                      <p className="text-sm text-slate-500">Total</p>

                      <p className="text-3xl font-bold text-violet-700">
                        ₹{cart.total_price}
                      </p>
                    </div>

                    <button
                      onClick={handleClearCart}
                      className="rounded-xl border border-rose-200 px-5 py-3 text-sm font-medium text-rose-500 transition hover:bg-rose-50"
                    >
                      Clear Cart
                    </button>
                  </div>
                </>
              )}
            </>
          )}
        </div>
      </div>
    </main>
  );
}
