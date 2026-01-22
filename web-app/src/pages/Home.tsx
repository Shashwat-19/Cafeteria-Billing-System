import { useEffect, useState } from 'react';
import api from '../lib/api';
import { MenuItem, CartItem } from '../types';
import { Navbar } from '../components/Navbar';
import { MenuCard } from '../components/MenuCard';
import { CartSidebar } from '../components/CartSidebar';
import { ShoppingBag, Loader2 } from 'lucide-react';
import { motion } from 'framer-motion';
import clsx from 'clsx';

const CATEGORIES = ["mains", "sides", "beverages", "desserts"];
const CATEGORY_LABELS: Record<string, string> = {
    mains: "🍽️ Main Dishes",
    sides: "🥗 Sides",
    beverages: "🥤 Beverages",
    desserts: "🍰 Desserts"
};

export const Home = () => {
  const [activeCategory, setActiveCategory] = useState("mains");
  const [menuItems, setMenuItems] = useState<MenuItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [cart, setCart] = useState<CartItem[]>([]);
  const [isCartOpen, setIsCartOpen] = useState(false);

  useEffect(() => {
    fetchMenu(activeCategory);
  }, [activeCategory]);

  const fetchMenu = async (category: string) => {
    setLoading(true);
    try {
      const response = await api.get<MenuItem[]>(`/menu/${category}`);
      setMenuItems(response.data);
    } catch (error) {
      console.error("Failed to fetch menu", error);
    } finally {
      setLoading(false);
    }
  };

  const addToCart = (item: MenuItem, quantity: number) => {
    setCart(prev => {
      // Check if item already exists
      const existing = prev.find(c => c.name === item.name); // Using name as unique identifier for now
      if (existing) {
        return prev.map(c => 
          c.name === item.name 
            ? { ...c, quantity: c.quantity + quantity, subtotal: (c.quantity + quantity) * c.price }
            : c
        );
      }
      return [...prev, { ...item, quantity, subtotal: item.price * quantity }];
    });
    setIsCartOpen(true);
  };

  const removeFromCart = (index: number) => {
    setCart(prev => prev.filter((_, i) => i !== index));
  };

  const handleCheckout = async () => {
    try {
      const orderData = {
        items: cart.map(item => ({
            name: item.name,
            price: item.price,
            quantity: item.quantity,
            subtotal: item.subtotal
        })),
        total_amount: cart.reduce((sum, item) => sum + item.subtotal, 0)
      };
      
      await api.post('/orders', orderData);
      alert('Order placed successfully!');
      setCart([]);
      setIsCartOpen(false);
    } catch (error) {
        console.error("Checkout failed", error);
        alert('Checkout failed!');
    }
  };

  const cartTotal = cart.reduce((sum, item) => sum + item.subtotal, 0);

  return (
    <div className="min-h-screen bg-background text-white pb-20">
      <Navbar />
      
      {/* Category Tabs */}
      <div className="sticky top-16 z-40 bg-background/80 backdrop-blur-md border-b border-white/5">
        <div className="container mx-auto px-4 overflow-x-auto no-scrollbar">
            <div className="flex gap-4 py-4 min-w-max">
                {CATEGORIES.map(cat => (
                    <button
                        key={cat}
                        onClick={() => setActiveCategory(cat)}
                        className={clsx(
                            "px-6 py-2 rounded-full text-sm font-medium transition-all duration-300",
                            activeCategory === cat 
                                ? "bg-primary text-white shadow-lg shadow-primary/25 scale-105" 
                                : "bg-secondary text-gray-400 hover:bg-white/5 hover:text-white"
                        )}
                    >
                        {CATEGORY_LABELS[cat]}
                    </button>
                ))}
            </div>
        </div>
      </div>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {loading ? (
            <div className="flex flex-col items-center justify-center py-20">
                <Loader2 className="w-10 h-10 animate-spin text-primary" />
                <p className="mt-4 text-gray-400">Loading menu...</p>
            </div>
        ) : (
            <motion.div 
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
                className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
            >
                {menuItems.map(item => (
                    <MenuCard key={item.id} item={item} onAdd={addToCart} />
                ))}
            </motion.div>
        )}
      </main>

      {/* Floating Cart Button */}
      <AnimatePresenceWrapper>
        {cart.length > 0 && (
            <motion.div
                initial={{ y: 100 }}
                animate={{ y: 0 }}
                className="fixed bottom-8 right-8 z-30"
            >
                <button
                    onClick={() => setIsCartOpen(true)}
                    className="bg-primary hover:bg-blue-600 text-white p-4 rounded-full shadow-2xl shadow-primary/40 flex items-center gap-3 transition-transform hover:scale-110 active:scale-95"
                >
                    <ShoppingBag className="w-6 h-6" />
                    <span className="font-bold">{cart.length}</span>
                </button>
            </motion.div>
        )}
      </AnimatePresenceWrapper>

      <CartSidebar 
        isOpen={isCartOpen} 
        onClose={() => setIsCartOpen(false)}
        cart={cart}
        onRemove={removeFromCart}
        onCheckout={handleCheckout}
        total={cartTotal}
      />
    </div>
  );
};

// Wrapper needed because AnimatePresence needs to be direct parent of motion.div? 
// No, just importing it.
const AnimatePresenceWrapper = ({ children }: { children: React.ReactNode }) => (
    <div className="relative z-30">{children}</div>
);
