import { MenuItem } from '../types';
import { Plus } from 'lucide-react';
import { useState } from 'react';
import clsx from 'clsx';

interface MenuCardProps {
  item: MenuItem;
  onAdd: (item: MenuItem, qty: number) => void;
}

export const MenuCard = ({ item, onAdd }: MenuCardProps) => {
  const [qty, setQty] = useState(1);

  return (
    <div className="group bg-secondary hover:bg-zinc-800 transition-all duration-300 rounded-xl overflow-hidden border border-white/5 hover:border-primary/50 relative">
        <div className="p-6">
            <div className="flex justify-between items-start mb-2">
                <div>
                    <h3 className="text-lg font-semibold text-white group-hover:text-primary transition-colors">
                        {item.name}
                    </h3>
                    <span className="text-xs uppercase tracking-wider text-gray-500 font-medium">{item.category}</span>
                </div>
                <span className="text-accent font-bold text-lg">${item.price.toFixed(2)}</span>
            </div>
            
            <p className="text-gray-400 text-sm mb-6 line-clamp-2 h-10">
                {item.description}
            </p>

            <div className="flex items-center justify-between gap-4 mt-auto">
                <div className="flex items-center bg-black/40 rounded-lg p-1">
                    <button 
                        onClick={() => setQty(Math.max(1, qty - 1))}
                        className="w-8 h-8 flex items-center justify-center text-gray-400 hover:text-white transition-colors"
                    >
                        -
                    </button>
                    <span className="w-8 text-center font-medium text-sm">{qty}</span>
                    <button 
                        onClick={() => setQty(Math.min(20, qty + 1))}
                        className="w-8 h-8 flex items-center justify-center text-gray-400 hover:text-white transition-colors"
                    >
                        +
                    </button>
                </div>

                <button
                    onClick={() => {
                        onAdd(item, qty);
                        setQty(1);
                    }}
                    className={clsx(
                        "flex-1 h-10 flex items-center justify-center gap-2 rounded-lg font-medium text-sm transition-all",
                        "bg-white text-black hover:bg-primary hover:text-white active:scale-95"
                    )}
                >
                    <Plus className="w-4 h-4" />
                    Add
                </button>
            </div>
        </div>
        
        {/* Glow effect */}
        <div className="absolute inset-0 bg-gradient-to-tr from-primary/10 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none" />
    </div>
  );
};
