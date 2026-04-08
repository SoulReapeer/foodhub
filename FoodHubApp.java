import java.util.*;

// ---------- MODELS ----------
class User {
    String name;
    String email;
    String password;

    User(String name, String email, String password) {
        this.name = name;
        this.email = email;
        this.password = password;
    }
}

class FoodItem {
    int id;
    String name;
    double price;

    FoodItem(int id, String name, double price) {
        this.id = id;
        this.name = name;
        this.price = price;
    }
}

class Restaurant {
    int id;
    String name;
    List<FoodItem> menu = new ArrayList<>();

    Restaurant(int id, String name) {
        this.id = id;
        this.name = name;
    }
}

class CartItem {
    FoodItem food;
    int quantity;

    CartItem(FoodItem food, int quantity) {
        this.food = food;
        this.quantity = quantity;
    }
}

class Order {
    List<CartItem> items;
    double total;
    String status;

    Order(List<CartItem> items, double total) {
        this.items = items;
        this.total = total;
        this.status = "Pending";
    }
}

// ---------- MAIN APP ----------
public class FoodHubApp {

    static Scanner sc = new Scanner(System.in);

    // Simulated Database
    static List<User> users = new ArrayList<>();
    static List<Restaurant> restaurants = new ArrayList<>();
    static List<Order> orders = new ArrayList<>();

    static User currentUser = null;
    static List<CartItem> cart = new ArrayList<>();

    public static void main(String[] args) {

        seedData(); // preload restaurants & food

        while (true) {
            System.out.println("\n==== FOOD HUB APP ====");
            System.out.println("1. Login");
            System.out.println("2. Signup");
            System.out.println("3. Exit");

            int choice = sc.nextInt();

            switch (choice) {
                case 1 -> login();
                case 2 -> signup();
                case 3 -> System.exit(0);
            }
        }
    }

    // ---------- AUTH ----------
    static void signup() {
        sc.nextLine();
        System.out.print("Enter Name: ");
        String name = sc.nextLine();
        System.out.print("Enter Email: ");
        String email = sc.nextLine();
        System.out.print("Enter Password: ");
        String pass = sc.nextLine();

        users.add(new User(name, email, pass));
        System.out.println("Signup Successful!");
    }

    static void login() {
        sc.nextLine();
        System.out.print("Email: ");
        String email = sc.nextLine();
        System.out.print("Password: ");
        String pass = sc.nextLine();

        for (User u : users) {
            if (u.email.equals(email) && u.password.equals(pass)) {
                currentUser = u;
                System.out.println("Login Successful!");
                homePage();
                return;
            }
        }

        System.out.println("Invalid Login!");
    }

    // ---------- HOME PAGE ----------
    static void homePage() {
        while (true) {
            System.out.println("\n==== HOME PAGE ====");
            for (Restaurant r : restaurants) {
                System.out.println(r.id + ". " + r.name);
            }
            System.out.println("0. Logout");

            int choice = sc.nextInt();
            if (choice == 0) return;

            for (Restaurant r : restaurants) {
                if (r.id == choice) {
                    restaurantPage(r);
                }
            }
        }
    }

    // ---------- RESTAURANT PAGE ----------
    static void restaurantPage(Restaurant r) {
        while (true) {
            System.out.println("\n== " + r.name + " Menu ==");
            for (FoodItem f : r.menu) {
                System.out.println(f.id + ". " + f.name + " - $" + f.price);
            }
            System.out.println("0. Back | 99. View Cart");

            int choice = sc.nextInt();

            if (choice == 0) return;
            if (choice == 99) {
                cartPage();
                continue;
            }

            for (FoodItem f : r.menu) {
                if (f.id == choice) {
                    System.out.print("Quantity: ");
                    int qty = sc.nextInt();
                    cart.add(new CartItem(f, qty));
                    System.out.println("Added to cart!");
                }
            }
        }
    }

    // ---------- CART PAGE ----------
    static void cartPage() {
        while (true) {
            System.out.println("\n==== CART ====");
            double total = 0;

            for (int i = 0; i < cart.size(); i++) {
                CartItem c = cart.get(i);
                double price = c.food.price * c.quantity;
                total += price;

                System.out.println((i + 1) + ". " + c.food.name +
                        " x" + c.quantity + " = $" + price);
            }

            System.out.println("Total: $" + total);
            System.out.println("1. Checkout");
            System.out.println("2. Back");

            int choice = sc.nextInt();

            if (choice == 1) {
                checkout(total);
                return;
            } else {
                return;
            }
        }
    }

    // ---------- CHECKOUT ----------
    static void checkout(double total) {
        System.out.println("\n==== CHECKOUT ====");
        sc.nextLine();
        System.out.print("Enter Address: ");
        String address = sc.nextLine();

        Order order = new Order(new ArrayList<>(cart), total);
        orders.add(order);

        cart.clear();

        System.out.println("Order Placed Successfully!");
        System.out.println("Status: " + order.status);

        orderPage();
    }

    // ---------- ORDER PAGE ----------
    static void orderPage() {
        System.out.println("\n==== YOUR ORDERS ====");

        for (Order o : orders) {
            System.out.println("Total: $" + o.total + " | Status: " + o.status);
        }
    }

    // ---------- SEED DATA ----------
    static void seedData() {
        Restaurant r1 = new Restaurant(1, "Pizza Palace");
        r1.menu.add(new FoodItem(1, "Pepperoni Pizza", 10));
        r1.menu.add(new FoodItem(2, "Cheese Pizza", 8));

        Restaurant r2 = new Restaurant(2, "Burger Hub");
        r2.menu.add(new FoodItem(1, "Beef Burger", 6));
        r2.menu.add(new FoodItem(2, "Chicken Burger", 5));

        restaurants.add(r1);
        restaurants.add(r2);
    }
}
