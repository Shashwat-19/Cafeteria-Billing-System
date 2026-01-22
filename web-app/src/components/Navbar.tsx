import { UtensilsCrossed } from 'lucide-react';

export const Navbar = () => {
  return (
    <nav className="h-16 border-b border-white/10 bg-secondary/50 backdrop-blur-md sticky top-0 z-50">
      <div className="container mx-auto h-full px-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="p-2 bg-primary rounded-lg">
            <UtensilsCrossed className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold bg-gradient-to-r from-blue-400 to-blue-200 bg-clip-text text-transparent">
              Cafeteria System
            </h1>
            <p className="text-xs text-gray-400">Premium Dining Experience</p>
          </div>
        </div>
        <div className="text-sm text-gray-400">
           {new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </div>
      </div>
    </nav>
  );
};
