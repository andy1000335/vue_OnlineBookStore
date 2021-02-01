import HomePage from './components/HomePage.vue'
import Shoppingcart from './components/Shoppingcart.vue'
import Login from './components/Login.vue'
import Register from './components/Register.vue'
import Account from './components/Account.vue'
import Book from './components/Book.vue'
import Checkout from './components/Checkout.vue'
import OrderManage from './components/OrderManage.vue'
import BookManage from './components/BookManage.vue'

export default [
    { path: '/', component: HomePage, name: 'home' },
    { path: '/shoppingcart', component: Shoppingcart, name: 'shoppingcart' },
    { path: '/login', component: Login, name: 'login' },
    { path: '/register', component: Register, name: 'register' },
    { path: '/account', component: Account, name: 'account' },
    { path: '/book/:isbn', component: Book, name: 'book' },
    { path: '/checkout', component: Checkout, name: 'checkout' },
    { path: '/order_manage', component: OrderManage, name: 'order_manage' },
    { path: '/book_manage', component: BookManage, name: 'book_manage' }
]