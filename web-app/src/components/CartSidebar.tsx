import { CartItem } from '../types';
import { X, Trash2, ShoppingBag } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface CartSidebarProps {
  isOpen: boolean;
  onClose: () => void;
  cart: CartItem[];
  onRemove: (index: number) => void;
  onCheckout: () => void;
  total: number;
}

export const CartSidebar = ({ isOpen, onClose, cart, onRemove, onCheckout, total }: CartSidebarProps) => {
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50"
          />
          <motion.div
            initial={{ x: '100%' }}
            animate={{ x: 0 }}
            exit={{ x: '100%' }}
            transition={{ type: 'spring', damping: 25, stiffness: 200 }}
            className="fixed right-0 top-0 h-full w-full max-w-md bg-secondary border-l border-white/10 z-50 flex flex-col shadow-2xl"
          >
            <div className="p-6 border-b border-white/10 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <ShoppingBag className="w-5 h-5 text-primary" />
                <h2 className="text-xl font-bold">Your Order</h2>
                <span className="bg-primary/20 text-primary text-xs px-2 py-1 rounded-full font-medium">
                  {cart.length} items
                </span>
              </div>
              <button onClick={onClose} className="p-2 hover:bg-white/5 rounded-lg transition-colors">
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="flex-1 overflow-y-auto p-6 space-y-4">
              {cart.length === 0 ? (
                <div className="h-full flex flex-col items-center justify-center text-gray-500 space-y-4">
                  <ShoppingBag className="w-16 h-16 opacity-20" />
                  <p>Your cart is empty</p>
                  <button onClick={onClose} className="text-primary text-sm hover:underline">
                    Browse Menu
                  </button>
                </div>
              ) : (
                cart.map((item, idx) => (
                  <motion.div
                    key={`${item.id}-${idx}`}
                    layout
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, scale: 0.95 }}
                    className="bg-black/40 rounded-xl p-4 flex gap-4 group relative overflow-hidden"
                  >
                   <div className="flex-1">
                      <div className="flex justify-between items-start">
                        <h4 className="font-medium text-white">{item.name}</h4>
                        <span className="text-sm font-bold text-accent">${item.subtotal.toFixed(2)}</span>
                      </div>
                      <div className="flex items-center gap-2 mt-2 text-sm text-gray-400">
                        <span>${item.price.toFixed(2)}</span>
                        <span>x</span>
                        <span className="text-white bg-white/10 px-2 rounded">{item.quantity}</span>
                      </div>
                   </div>
                   <button
                      onClick={() => onRemove(idx)}
                      className="p-2 text-gray-500 hover:text-red-500 hover:bg-red-500/10 rounded-lg transition-all opacity-0 group-hover:opacity-100"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </motion.div>
                ))
              )}
            </div>

            <div className="p-6 bg-black/40 border-t border-white/10 space-y-4">
              <div className="space-y-2">
                <div className="flex justify-between text-gray-400">
                  <span>Subtotal</span>
                  <span>${total.toFixed(2)}</span>
                </div>
                <div className="flex justify-between text-xl font-bold text-white pt-2 border-t border-white/10">
                  <span>Total</span>
                  <span>${total.toFixed(2)}</span>
                </div>
              </div>
              <button
                onClick={onCheckout}
                disabled={cart.length === 0}
                className="w-full py-4 bg-primary hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-xl font-bold text-lg shadow-lg shadow-blue-500/20 transition-all hover:scale-[1.02] active:scale-[0.98]"
              >
                Checkout
              </button>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
};
