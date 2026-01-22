export interface MenuItem {
    id: number;
    name: string;
    category: string;
    price: number;
    description: string;
    image_url?: string;
}

export interface OrderItem {
    name: string;
    price: number;
    quantity: number;
    subtotal: number;
}

export interface Order {
    id: number;
    total_amount: number;
    status: string;
}

export type CartItem = MenuItem & { quantity: number; subtotal: number };
