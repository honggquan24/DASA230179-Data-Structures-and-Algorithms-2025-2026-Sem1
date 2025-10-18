import streamlit as st
from datetime import datetime, timedelta
import math
import heapq

# CLASSES 
class Driver:
    def __init__(self, id, name, rating, x, y, trips=0, experience=0):
        self.id = id
        self.name = name
        self.rating = rating
        self.x = x
        self.y = y
        self.trips = trips
        self.experience = experience
    
    def __str__(self):
        return f"ID: {self.id}, Ten: {self.name}, Rating: {self.rating}, Toa do: ({self.x}, {self.y})"
    
    def to_dict(self):
        return {
            'ID': self.id,
            'Ten': self.name,
            'Rating': self.rating,
            'X': self.x,
            'Y': self.y,
            'Trips': self.trips,
            'Experience': self.experience
        }
    
class DriverManagementSystem:
    def __init__(self):
        self.drivers = []    
        self.id_index = {}      
        self.next_id = 1
    
    def load_from_file(self, filename="drivers.csv"):
        """Đọc dữ liệu từ file CSV"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f.readlines()[1:]:
                    parts = [p.strip() for p in line.strip().split(',')]
                    if len(parts) >= 5:
                        driver = Driver(
                            int(parts[0]), 
                            parts[1], 
                            float(parts[2]), 
                            float(parts[3]), 
                            float(parts[4]),
                            int(parts[5]) if len(parts) > 5 else 0,
                            int(parts[6]) if len(parts) > 6 else 0
                        )
                        self.drivers.append(driver)
                        self.id_index[driver.id] = driver
                        self.next_id = max(self.next_id, driver.id + 1)
            st.success(f"Da tai {len(self.drivers)} tai xe tu file")
        except FileNotFoundError:
            st.warning(f"Khong tim thay file {filename}. Su dung du lieu mau.")
            self._load_sample_data()
        return self
    
    def _load_sample_data(self):
        """Tải dữ liệu mẫu nếu không có file"""
        sample_drivers = [
            Driver(1, "Nguyen Van A", 4.5, 10.8231, 106.6297, 120, 5),
            Driver(2, "Tran Van B", 4.8, 10.7769, 106.7009, 85, 3),
            Driver(3, "Le Van C", 4.2, 10.8050, 106.6500, 200, 7)
        ]
        for driver in sample_drivers:
            self.drivers.append(driver)
            self.id_index[driver.id] = driver
            self.next_id = max(self.next_id, driver.id + 1)
    
    def save_to_file(self, filename="drivers.csv"):
        """Lưu dữ liệu vào file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("ID,Name,Rating,X,Y,Trips,Experience\n")
                for d in self.drivers:
                    f.write(f"{d.id},{d.name},{d.rating},{d.x},{d.y},{d.trips},{d.experience}\n")
            st.success(f"Da luu {len(self.drivers)} tai xe vao file")
        except Exception as e:
            st.error(f"Loi khi luu file: {e}")
    
    def get_all_drivers(self):
        """Lấy danh sách tất cả tài xế"""
        return [d.to_dict() for d in self.drivers]
    
    def display_all(self):
        """Hiển thị toàn bộ danh sách"""
        if not self.drivers:
            st.info("Danh sach trong!")
            return
        return self.get_all_drivers()
    
    def display_top_k(self, k, from_top=True):
        """Hiển thị top k tài xế"""
        if not self.drivers:
            return []
        k = min(k, len(self.drivers))
        show = self.drivers[:k] if from_top else self.drivers[-k:]
        return [d.to_dict() for d in show]
    
    def add_driver(self, name, rating, x, y, trips=0, experience=0):
        """Thêm tài xế mới - O(1)"""
        driver = Driver(self.next_id, name, rating, x, y, trips, experience)
        self.drivers.append(driver)
        self.id_index[driver.id] = driver
        self.next_id += 1
        return driver
    
    def search_driver(self, keyword):
        """Tìm kiếm theo ID (O(1)) hoặc tên (O(n))"""
        try:
            id_val = int(keyword)
            if id_val in self.id_index:
                return [self.id_index[id_val].to_dict()]
        except ValueError:
            pass
        
        results = [d.to_dict() for d in self.drivers if keyword.lower() in d.name.lower()]
        return results
    
    def update_driver(self, id, new_name=None, new_rating=None, new_x=None, new_y=None, new_trips=None, new_experience=None):
        """Cập nhật thông tin tài xế - O(1) tìm, O(1) cập nhật"""
        if id not in self.id_index:
            return False
        
        driver = self.id_index[id]
        if new_name: driver.name = new_name
        if new_rating is not None: driver.rating = new_rating
        if new_x is not None: driver.x = new_x
        if new_y is not None: driver.y = new_y
        if new_trips is not None: driver.trips = new_trips
        if new_experience is not None: driver.experience = new_experience
        return True
    
    def delete_driver(self, id):
        """Xóa tài xế - O(1) tìm, O(n) xóa khỏi list"""
        if id not in self.id_index:
            return False
        
        driver = self.id_index[id]
        self.drivers.remove(driver)
        del self.id_index[id]
        return True
    
    def quick_sort(self, arr, ascending=False):
        """Quick Sort theo rating - O(n log n)"""
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        if ascending:
            left = [x for x in arr if x.rating < pivot.rating]
            middle = [x for x in arr if x.rating == pivot.rating]
            right = [x for x in arr if x.rating > pivot.rating]
        else:
            left = [x for x in arr if x.rating > pivot.rating]
            middle = [x for x in arr if x.rating == pivot.rating]
            right = [x for x in arr if x.rating < pivot.rating]
        return self.quick_sort(left, ascending) + middle + self.quick_sort(right, ascending)
    
    def sort_by_rating(self, ascending=False):
        """Sắp xếp theo rating"""
        if not self.drivers:
            return
        self.drivers = self.quick_sort(self.drivers, ascending)

# CUSTOMER CLASSES 
class Customer:
    def __init__(self, cid, name, location, x, y):
        self.id = cid
        self.name = name
        self.location = location
        self.x = x
        self.y = y
    
    def __str__(self):
        return f"ID: {self.id}, Ten: {self.name}, Quan: {self.location}, Toa do: ({self.x}, {self.y})"
    
    def to_dict(self):
        return {
            'ID': self.id,
            'Ten': self.name,
            'Quan': self.location,
            'X': self.x,
            'Y': self.y
        }

class CustomerManagementSystem:
    def __init__(self):
        self.customers = {}
        self.next_id = 1
    
    def load_from_file(self, filename="customers.csv"):
        """Đọc dữ liệu từ file CSV"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f.readlines()[1:]:
                    parts = [p.strip() for p in line.strip().split(',')]
                    if len(parts) >= 5:
                        customer = Customer(int(parts[0]), parts[1], parts[2], float(parts[3]), float(parts[4]))
                        self.customers[customer.id] = customer
                        self.next_id = max(self.next_id, customer.id + 1)
            st.success(f"Da tai {len(self.customers)} khach hang tu file")
        except FileNotFoundError:
            st.warning(f"Khong tim thay file {filename}. Su dung du lieu mau.")
            self._load_sample_data()
        return self
    
    def _load_sample_data(self):
        """Tải dữ liệu mẫu nếu không có file"""
        sample_customers = [
            Customer(1, "Nguyen Thi Hoa", "Quan 1", 10.7756, 106.7019),
            Customer(2, "Tran Van Minh", "Quan 3", 10.7889, 106.7050),
            Customer(3, "Le Thi Lan", "Quan 1", 10.7650, 106.6950),
            Customer(4, "Pham Van Nam", "Quan 2", 10.7800, 106.7100),
            Customer(5, "Vo Thi Mai", "Quan 1", 10.7700, 106.7000)
        ]
        for customer in sample_customers:
            self.customers[customer.id] = customer
            self.next_id = max(self.next_id, customer.id + 1)
    
    def save_to_file(self, filename="customers.csv"):
        """Lưu dữ liệu vào file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("ID,Name,Location,X,Y\n")
                for c in self.customers.values():
                    f.write(f"{c.id},{c.name},{c.location},{c.x},{c.y}\n")
            st.success(f"Da luu {len(self.customers)} khach hang vao file")
        except Exception as e:
            st.error(f"Loi khi luu file: {e}")
    
    def add_customer(self, name, location, x, y):
        """Thêm khách hàng mới - O(1)"""
        if not name or not location:
            return None
        customer = Customer(self.next_id, name, location, x, y)
        self.customers[customer.id] = customer
        self.next_id += 1
        return customer
    
    def update_customer(self, cid, name=None, location=None, x=None, y=None):
        """Cập nhật thông tin khách hàng - O(1)"""
        if cid not in self.customers:
            return False
        c = self.customers[cid]
        if name: c.name = name
        if location: c.location = location
        if x is not None: c.x = x
        if y is not None: c.y = y
        return True
    
    def delete_customer(self, cid):
        """Xóa khách hàng - O(1)"""
        if cid in self.customers:
            del self.customers[cid]
            return True
        return False
    
    def search_by_id(self, cid):
        """Tìm khách hàng theo ID - O(1)"""
        return self.customers.get(cid, None)
    
    def search_by_name(self, name):
        """Tìm khách hàng theo tên - O(n)"""
        results = []
        for c in self.customers.values():
            if name.lower() in c.name.lower():
                results.append(c)
        return results
    
    def search_customer(self, keyword):
        """Tìm kiếm theo ID hoặc tên"""
        try:
            cid = int(keyword)
            customer = self.search_by_id(cid)
            return [customer.to_dict()] if customer else []
        except ValueError:
            results = self.search_by_name(keyword)
            return [c.to_dict() for c in results]
    
    def top_k_customers(self, k, from_top=True):
        """Hiển thị top k khách hàng theo ID"""
        if not self.customers:
            return []
        sorted_customers = sorted(self.customers.values(), key=lambda c: c.id)
        if from_top:
            return [c.to_dict() for c in sorted_customers[:k]]
        else:
            return [c.to_dict() for c in sorted_customers[-k:]]
    
    def list_by_location(self, location, limit=10):
        """Liệt kê khách hàng theo quận"""
        filtered = [c for c in self.customers.values() if location.lower() in c.location.lower()]
        filtered.sort(key=lambda c: c.id)
        if limit:
            return [c.to_dict() for c in filtered[:limit]], len(filtered)
        return [c.to_dict() for c in filtered], len(filtered)
    
    def get_all_customers(self):
        """Lấy danh sách tất cả khách hàng"""
        return [c.to_dict() for c in self.customers.values()]

# RIDE CLASSES
class Ride:
    def __init__(self, ride_id, customer_id, driver_id, distance, fare, start_time=None, end_time=None, start_point="", end_point=""):
        self.ride_id = ride_id
        self.customer_id = customer_id
        self.driver_id = driver_id
        self.distance = distance
        self.fare = fare
        self.start_time = start_time if start_time else datetime.now()
        self.end_time = end_time if end_time else datetime.now()
        self.start_point = start_point
        self.end_point = end_point
    
    def __str__(self):
        return f"Ride ID: {self.ride_id}, Driver: {self.driver_id}, Customer: {self.customer_id}, Distance: {self.distance}km, Fare: {self.fare}"
    
    def to_dict(self):
        return {
            'RideID': self.ride_id,
            'CustomerID': self.customer_id,
            'DriverID': self.driver_id,
            'Distance': self.distance,
            'Fare': self.fare,
            'StartTime': self.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'EndTime': self.end_time.strftime('%Y-%m-%d %H:%M:%S'),
            'StartPoint': self.start_point,
            'EndPoint': self.end_point
        }

class RideManagementSystem:
    def __init__(self):
        self.rides = []
        self.driver_rides = {}
        self.next_id = 1
    
    def load_from_file(self, filename="rides.csv"):
        """Đọc dữ liệu từ file CSV"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f.readlines()[1:]:
                    parts = [p.strip() for p in line.strip().split(',')]
                    if len(parts) >= 5:
                        ride_id = int(parts[0])
                        customer_id = parts[1]
                        driver_id = int(parts[2])
                        distance = float(parts[3])
                        fare = float(parts[4])
                        
                        start_time = datetime(2024, 10, ride_id % 28 + 1, (ride_id * 2) % 24, (ride_id * 15) % 60)
                        end_time = datetime(2024, 10, ride_id % 28 + 1, ((ride_id * 2) % 24 + 1) % 24, (ride_id * 20) % 60)
                        
                        ride = Ride(ride_id, customer_id, driver_id, distance, fare, start_time, end_time, "Diem A", "Diem B")
                        self.rides.append(ride)
                        
                        if driver_id not in self.driver_rides:
                            self.driver_rides[driver_id] = []
                        self.driver_rides[driver_id].append(ride)
                        
                        self.next_id = max(self.next_id, ride_id + 1)
            st.success(f"Da tai {len(self.rides)} chuyen di tu file")
        except FileNotFoundError:
            st.warning(f"Khong tim thay file {filename}. Su dung du lieu mau.")
            self._load_sample_data()
        return self
    
    def _load_sample_data(self):
        """Tải dữ liệu mẫu"""
        sample_rides = [
            Ride(1, "C8", 9, 88.8, 765900, datetime(2024, 10, 1, 8, 30), datetime(2024, 10, 1, 9, 15), "Quan 1", "Quan 5"),
            Ride(2, "C6", 6, 39.9, 342940, datetime(2024, 10, 2, 14, 0), datetime(2024, 10, 2, 15, 10), "Quan 5", "Thu Duc"),
            Ride(3, "C5", 9, 69.7, 523934, datetime(2024, 9, 29, 7, 0), datetime(2024, 9, 29, 7, 45), "Tan Binh", "Quan 3"),
            Ride(4, "C5", 4, 63.0, 460593, datetime(2024, 10, 3, 10, 20), datetime(2024, 10, 3, 11, 30), "Quan 2", "Quan 7"),
            Ride(5, "C6", 2, 30.7, 234885, datetime(2024, 10, 4, 16, 45), datetime(2024, 10, 4, 17, 30), "Quan 3", "Quan 1"),
        ]
        for ride in sample_rides:
            self.rides.append(ride)
            if ride.driver_id not in self.driver_rides:
                self.driver_rides[ride.driver_id] = []
            self.driver_rides[ride.driver_id].append(ride)
            self.next_id = max(self.next_id, ride.ride_id + 1)
    
    def save_to_file(self, filename="rides.csv"):
        """Lưu dữ liệu vào file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("RideID,CustomerID,DriverID,Distance(km),Fare(VND)\n")
                for r in self.rides:
                    f.write(f"{r.ride_id},{r.customer_id},{r.driver_id},{r.distance},{r.fare}\n")
            st.success(f"Da luu {len(self.rides)} chuyen di vao file")
        except Exception as e:
            st.error(f"Loi khi luu file: {e}")
    
    def get_driver_trips(self, driver_id, ascending=True):
        """Lấy danh sách chuyến đi của tài xế - O(1) lookup + O(n log n) sort"""
        if driver_id not in self.driver_rides:
            return []
        trips = self.driver_rides[driver_id].copy()
        trips.sort(key=lambda x: x.start_time, reverse=not ascending)
        return [t.to_dict() for t in trips]
    
    def filter_trips_by_time(self, driver_id, start_date, end_date):
        """Lọc chuyến đi theo khoảng thời gian"""
        if driver_id not in self.driver_rides:
            return []
        
        trips = self.driver_rides[driver_id]
        filtered = []
        
        for trip in trips:
            if start_date <= trip.start_time <= end_date:
                filtered.append(trip)
        
        filtered.sort(key=lambda x: x.start_time)
        return [t.to_dict() for t in filtered]
    
    def get_recent_trips(self, driver_id, limit=10):
        """Lấy n chuyến đi gần nhất"""
        if driver_id not in self.driver_rides:
            return []
        trips = self.driver_rides[driver_id].copy()
        trips.sort(key=lambda x: x.start_time, reverse=True)
        return [t.to_dict() for t in trips[:limit]]
    
    def get_all_rides(self):
        """Lấy tất cả chuyến đi"""
        return [r.to_dict() for r in self.rides]

# FIND DRIVER SYSTEM  
class FindDriverSystem:
    def __init__(self, driver_manager, customer_manager):
        self.driver_manager = driver_manager
        self.customer_manager = customer_manager
    
    def calculate_distance(self, x1, y1, x2, y2):
        """Tính khoảng cách Euclidean"""
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    def find_drivers_within_radius(self, customer_id, radius, sort_priority=None, 
                                   top_k=None, min_rating=None, min_trips=None, min_experience=None):
        """
        Tìm tài xế trong bán kính
        
        sort_priority: list các tiêu chí ['distance', '-rating', 'trips', '-experience']
                      Dấu '-' nghĩa là giảm dần
        """
        # Kiểm tra khách hàng
        if customer_id not in self.customer_manager.customers:
            return [], f"Khach hang ID {customer_id} khong ton tai"
        
        customer = self.customer_manager.customers[customer_id]
        cust_x, cust_y = customer.x, customer.y
        
        # Tìm tài xế trong bán kính
        candidates = []
        for driver in self.driver_manager.drivers:
            distance = self.calculate_distance(cust_x, cust_y, driver.x, driver.y)
            
            if distance <= radius:
                # Áp dụng bộ lọc
                if min_rating and driver.rating < min_rating:
                    continue
                if min_trips and driver.trips < min_trips:
                    continue
                if min_experience and driver.experience < min_experience:
                    continue
                
                candidates.append({
                    'driver': driver,
                    'distance': distance
                })
        
        if not candidates:
            return [], None
        
        # Sắp xếp theo priority
        if sort_priority:
            def get_sort_key(item):
                keys = []
                for criterion in sort_priority:
                    reverse = criterion.startswith('-')
                    field = criterion.lstrip('-')
                    
                    if field == 'distance':
                        value = item['distance']
                    elif field == 'rating':
                        value = item['driver'].rating
                    elif field == 'trips':
                        value = item['driver'].trips
                    elif field == 'experience':
                        value = item['driver'].experience
                    else:
                        value = 0
                    
                    keys.append(-value if reverse else value)
                return tuple(keys)
            
            candidates.sort(key=get_sort_key)
        
        # Top K
        if top_k:
            candidates = candidates[:top_k]
        
        # Chuyển đổi kết quả
        results = []
        for item in candidates:
            driver = item['driver']
            result = driver.to_dict()
            result['Distance'] = item['distance']
            results.append(result)
        
        return results, None

# BOOKING SYSTEM 
class BookingSystem:
    def __init__(self, driver_manager, customer_manager, ride_manager):
        self.driver_manager = driver_manager
        self.customer_manager = customer_manager
        self.ride_manager = ride_manager
        self.pending_bookings = []  # Danh sách chuyến đang chờ
        self.FARE_RATE = 12000  # 12,000 VND/km
    
    def get_driver_location(self, driver_id):
        """Lấy vị trí tài xế"""
        if driver_id in self.driver_manager.id_index:
            driver = self.driver_manager.id_index[driver_id]
            return driver.x, driver.y, driver.name
        return None, None, None
    
    def get_customer_location(self, customer_id):
        """Lấy vị trí khách hàng"""
        if customer_id in self.customer_manager.customers:
            customer = self.customer_manager.customers[customer_id]
            return customer.x, customer.y, customer.name
        return None, None, None
    
    def calculate_distance(self, x1, y1, x2, y2):
        """Tính khoảng cách giữa 2 điểm"""
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    
    def estimate_time(self, distance):
        """Ước tính thời gian (giả định tốc độ 40 km/h)"""
        speed = 40  # km/h
        time_hours = distance / speed
        time_minutes = time_hours * 60
        return int(time_minutes)
    
    def create_booking(self, customer_id, driver_id, trip_distance):
        """Tạo booking mới"""
        # Lấy thông tin khách hàng
        cust_x, cust_y, cust_name = self.get_customer_location(customer_id)
        if cust_x is None:
            return None, f"Khach hang ID {customer_id} khong ton tai"
        
        # Lấy thông tin tài xế
        driver_x, driver_y, driver_name = self.get_driver_location(driver_id)
        if driver_x is None:
            return None, f"Tai xe ID {driver_id} khong ton tai"
        
        # Tính khoảng cách từ tài xế đến khách hàng
        pickup_distance = self.calculate_distance(driver_x, driver_y, cust_x, cust_y)
        
        # Tính tổng khoảng cách và giá cước
        total_distance = pickup_distance + trip_distance
        fare = total_distance * self.FARE_RATE
        
        # Ước tính thời gian
        pickup_time = self.estimate_time(pickup_distance)
        trip_time = self.estimate_time(trip_distance)
        total_time = pickup_time + trip_time
        
        # Tạo booking object
        booking = {
            'booking_id': len(self.pending_bookings) + 1,
            'customer_id': customer_id,
            'customer_name': cust_name,
            'customer_location': (cust_x, cust_y),
            'driver_id': driver_id,
            'driver_name': driver_name,
            'driver_location': (driver_x, driver_y),
            'pickup_distance': pickup_distance,
            'trip_distance': trip_distance,
            'total_distance': total_distance,
            'fare': fare,
            'pickup_time': pickup_time,
            'trip_time': trip_time,
            'total_time': total_time,
            'status': 'Pending',
            'created_at': datetime.now(),
            'cancel_reason': None
        }
        
        self.pending_bookings.append(booking)
        return booking, None
    
    def confirm_booking(self, booking_id):
        """Xác nhận chuyến đi"""
        for booking in self.pending_bookings:
            if booking['booking_id'] == booking_id and booking['status'] == 'Pending':
                # Import Ride class (cần có sẵn)
                from your_module import Ride  # Thay thế bằng import thực tế
                
                # Tạo ride mới
                ride = Ride(
                    ride_id=self.ride_manager.next_id,
                    customer_id=booking['customer_id'],
                    driver_id=booking['driver_id'],
                    distance=booking['total_distance'],
                    fare=booking['fare'],
                    start_time=booking['created_at'],
                    end_time=booking['created_at'] + timedelta(minutes=booking['total_time']),
                    start_point=f"({booking['customer_location'][0]:.4f}, {booking['customer_location'][1]:.4f})",
                    end_point="Diem den"
                )
                
                # Lưu vào ride manager
                self.ride_manager.rides.append(ride)
                if ride.driver_id not in self.ride_manager.driver_rides:
                    self.ride_manager.driver_rides[ride.driver_id] = []
                self.ride_manager.driver_rides[ride.driver_id].append(ride)
                self.ride_manager.next_id += 1
                
                # Cập nhật trạng thái booking
                booking['status'] = 'Confirmed'
                booking['confirmed_at'] = datetime.now()
                booking['ride_id'] = ride.ride_id
                
                return True, f"Da xac nhan chuyen di. Ride ID: {ride.ride_id}"
        
        return False, "Khong tim thay booking hoac booking da duoc xu ly"
    
    def cancel_booking(self, booking_id, reason=""):
        """Hủy chuyến đi"""
        for booking in self.pending_bookings:
            if booking['booking_id'] == booking_id and booking['status'] == 'Pending':
                booking['status'] = 'Canceled'
                booking['canceled_at'] = datetime.now()
                booking['cancel_reason'] = reason if reason else "Khong co ly do"
                return True, "Da huy chuyen di"
        
        return False, "Khong tim thay booking hoac booking da duoc xu ly"
    
    def get_pending_bookings(self):
        """Lấy danh sách chuyến đang chờ"""
        return [b for b in self.pending_bookings if b['status'] == 'Pending']
    
    def get_all_bookings(self):
        """Lấy tất cả bookings"""
        return self.pending_bookings
    
    def confirm_all_pending(self):
        """Xác nhận tất cả chuyến đang chờ"""
        confirmed_count = 0
        for booking in self.pending_bookings:
            if booking['status'] == 'Pending':
                success, _ = self.confirm_booking(booking['booking_id'])
                if success:
                    confirmed_count += 1
        return confirmed_count
    
    def cancel_all_pending(self):
        """Hủy tất cả chuyến đang chờ"""
        canceled_count = 0
        for booking in self.pending_bookings:
            if booking['status'] == 'Pending':
                success, _ = self.cancel_booking(booking['booking_id'], "Huy tat ca")
                if success:
                    canceled_count += 1
        return canceled_count

# AUTO MATCHING SYSTEM 
class RideRequest:
    def __init__(self, request_id, customer_id, customer_location, trip_distance, state="waiting"):
        self.request_id = request_id
        self.customer_id = customer_id
        self.customer_location = customer_location
        self.trip_distance = trip_distance
        self.state = state  # waiting | matching | matched | failed
        self.assigned_driver_id = None
        self.assigned_driver_name = None
        self.created_at = datetime.now()
    
    def __repr__(self):
        return f"RideRequest({self.request_id}, state={self.state}, driver={self.assigned_driver_id})"
    
    def to_dict(self):
        return {
            'RequestID': self.request_id,
            'CustomerID': self.customer_id,
            'State': self.state,
            'DriverID': self.assigned_driver_id,
            'DriverName': self.assigned_driver_name,
            'TripDistance': self.trip_distance,
            'CreatedAt': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class AutoMatchingSystem:
    def __init__(self, driver_manager, customer_manager, booking_system):
        self.driver_manager = driver_manager
        self.customer_manager = customer_manager
        self.booking_system = booking_system
        self.ride_requests = []
        self.next_request_id = 1
        self.busy_drivers = set()  # Tập tài xế đang bận
    
    def distance(self, loc1, loc2):
        """Tính khoảng cách Euclidean"""
        return math.sqrt((loc1[0] - loc2[0])**2 + (loc1[1] - loc2[1])**2)
    
    def create_ride_request(self, customer_id, trip_distance):
        """Tạo yêu cầu đặt xe mới"""
        # Kiểm tra khách hàng
        if customer_id not in self.customer_manager.customers:
            return None, f"Khach hang ID {customer_id} khong ton tai"
        
        customer = self.customer_manager.customers[customer_id]
        customer_location = (customer.x, customer.y)
        
        # Tạo request
        request = RideRequest(
            request_id=self.next_request_id,
            customer_id=customer_id,
            customer_location=customer_location,
            trip_distance=trip_distance
        )
        
        self.ride_requests.append(request)
        self.next_request_id += 1
        
        return request, None
    
    def get_available_drivers(self):
        """Lấy danh sách tài xế khả dụng (không bận)"""
        return [d for d in self.driver_manager.drivers if d.id not in self.busy_drivers]
    
    def calculate_driver_score(self, driver, customer_location):
        """
        Tính điểm đánh giá tài xế (điểm càng cao càng tốt)
        
        Công thức: Score = -(w1*distance - w2*rating - w3*(1/trips))
        - w1 = 0.6: Trọng số khoảng cách (ưu tiên gần)
        - w2 = 0.3: Trọng số rating (ưu tiên rating cao)
        - w3 = 0.1: Trọng số phân bổ đều (ưu tiên tài xế ít chuyến)
        """
        dist = self.distance((driver.x, driver.y), customer_location)
        
        # Chuẩn hóa các giá trị về cùng thang đo
        normalized_distance = dist / 10.0  # Giả định khoảng cách max ~10km
        normalized_rating = driver.rating / 5.0  # Rating từ 0-5
        normalized_trips = 1.0 / (driver.trips + 1)  # Nghịch đảo số chuyến
        
        # Tính điểm (điểm càng cao càng tốt)
        score = -(0.6 * normalized_distance) + (0.3 * normalized_rating) + (0.1 * normalized_trips)
        
        return score, dist
    
    def find_best_driver(self, request):
        """Tìm tài xế phù hợp nhất cho yêu cầu"""
        available_drivers = self.get_available_drivers()
        
        if not available_drivers:
            return None, None, "Khong co tai xe kha dung"
        
        # Tính điểm cho từng tài xế
        driver_scores = []
        for driver in available_drivers:
            score, distance = self.calculate_driver_score(driver, request.customer_location)
            driver_scores.append((driver, score, distance))
        
        # Sắp xếp theo điểm giảm dần (điểm cao nhất = tốt nhất)
        driver_scores.sort(key=lambda x: x[1], reverse=True)
        
        best_driver, best_score, distance = driver_scores[0]
        
        return best_driver, distance, None
    
    def assign_driver(self, request_id):
        """Ghép tài xế cho yêu cầu"""
        # Tìm request
        request = None
        for r in self.ride_requests:
            if r.request_id == request_id:
                request = r
                break
        
        if not request:
            return False, "Khong tim thay request"
        
        if request.state != "waiting":
            return False, f"Request da duoc xu ly (trang thai: {request.state})"
        
        # Bắt đầu matching
        request.state = "matching"
        
        # Tìm tài xế tốt nhất
        best_driver, distance, error = self.find_best_driver(request)
        
        if error:
            request.state = "failed"
            return False, error
        
        # Gán tài xế
        request.state = "matched"
        request.assigned_driver_id = best_driver.id
        request.assigned_driver_name = best_driver.name
        
        # Đánh dấu tài xế bận
        self.busy_drivers.add(best_driver.id)
        
        # Tạo booking tự động
        booking, error = self.booking_system.create_booking(
            customer_id=request.customer_id,
            driver_id=best_driver.id,
            trip_distance=request.trip_distance
        )
        
        return True, {
            'request': request,
            'driver': best_driver,
            'distance': distance,
            'booking': booking
        }
    
    def auto_assign_all(self):
        """Tự động ghép tất cả request đang chờ"""
        waiting_requests = [r for r in self.ride_requests if r.state == "waiting"]
        
        results = {
            'success': 0,
            'failed': 0,
            'details': []
        }
        
        for request in waiting_requests:
            success, result = self.assign_driver(request.request_id)
            if success:
                results['success'] += 1
                results['details'].append({
                    'request_id': request.request_id,
                    'customer_id': request.customer_id,
                    'driver_id': request.assigned_driver_id,
                    'driver_name': request.assigned_driver_name,
                    'status': 'matched'
                })
            else:
                results['failed'] += 1
                results['details'].append({
                    'request_id': request.request_id,
                    'customer_id': request.customer_id,
                    'status': 'failed',
                    'reason': result
                })
        
        return results
    
    def release_driver(self, driver_id):
        """Giải phóng tài xế (đánh dấu rảnh)"""
        if driver_id in self.busy_drivers:
            self.busy_drivers.remove(driver_id)
    
    def get_all_requests(self):
        """Lấy tất cả requests"""
        return [r.to_dict() for r in self.ride_requests]
    
    def get_waiting_requests(self):
        """Lấy requests đang chờ"""
        return [r.to_dict() for r in self.ride_requests if r.state == "waiting"]

# UNDO SYSTEM
class Action:
    """Lưu thông tin một thao tác"""
    def __init__(self, action_type, entity_type, data, timestamp=None):
        self.type = action_type      # 'ADD', 'UPDATE', 'DELETE'
        self.entity_type = entity_type  # 'DRIVER', 'CUSTOMER', 'RIDE', 'BOOKING'
        self.data = data              # Dữ liệu cần để undo
        self.timestamp = timestamp or datetime.now()
    
    def __str__(self):
        return f"[{self.timestamp.strftime('%H:%M:%S')}] {self.entity_type}.{self.type}: {self.data.get('id', 'N/A')}"
    
    def to_dict(self):
        return {
            'type': self.type,
            'entity_type': self.entity_type,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'data': str(self.data)
        }

class UndoStack:
    """Stack lưu lịch sử thao tác - LIFO"""
    
    def __init__(self, max_size=10):
        self.stack = []
        self.max_size = max_size
    
    def push(self, action):
        """Thêm thao tác vào stack - O(1)"""
        self.stack.append(action)
        
        # Xóa thao tác cũ nhất nếu vượt giới hạn
        if len(self.stack) > self.max_size:
            self.stack.pop(0)
    
    def pop(self):
        """Lấy và xóa thao tác cuối - O(1)"""
        if self.is_empty():
            return None
        return self.stack.pop()
    
    def peek(self):
        """Xem thao tác cuối mà không xóa - O(1)"""
        if self.is_empty():
            return None
        return self.stack[-1]
    
    def is_empty(self):
        """Kiểm tra stack rỗng - O(1)"""
        return len(self.stack) == 0
    
    def size(self):
        """Số thao tác trong stack - O(1)"""
        return len(self.stack)
    
    def clear(self):
        """Xóa toàn bộ lịch sử - O(1)"""
        self.stack = []
    
    def get_history(self):
        """Lấy danh sách lịch sử"""
        return [action.to_dict() for action in reversed(self.stack)]

# MANAGE SESSION STATE
class ManageSessionState:
    def __init__(self):
        # Khởi tạo driver manager
        if 'driver_manager' not in st.session_state:
            driver_manager = DriverManagementSystem()
            driver_manager.load_from_file("drivers.csv")
            st.session_state.driver_manager = driver_manager
        
        # Khởi tạo customer manager
        if 'customer_manager' not in st.session_state:
            customer_manager = CustomerManagementSystem()
            customer_manager.load_from_file("customers.csv")
            st.session_state.customer_manager = customer_manager
        
        # Khởi tạo ride manager
        if 'ride_manager' not in st.session_state:
            ride_manager = RideManagementSystem()
            ride_manager.load_from_file("rides.csv")
            st.session_state.ride_manager = ride_manager

        # Khởi tạo history cho undo
        if 'history' not in st.session_state:
            st.session_state.history = []

    def get_driver_manager(self):
        return st.session_state.driver_manager
    
    def get_customer_manager(self):
        return st.session_state.customer_manager
    
    def get_ride_manager(self):
        return st.session_state.ride_manager

    def save_state(self):
        """Lưu snapshot toàn bộ state trước khi thay đổi"""
        current_state = {
            'drivers': [d.to_dict() for d in st.session_state.driver_manager.drivers],
            'customers': {cid: c.to_dict() for cid, c in st.session_state.customer_manager.customers.items()},
            'rides': [r.to_dict() for r in st.session_state.ride_manager.rides]
        }
        st.session_state.history.append(current_state)
        
        # Giới hạn lịch sử tối đa 10 bước
        if len(st.session_state.history) > 10:
            st.session_state.history.pop(0)

    def undo(self):
        """Khôi phục state trước đó"""
        if st.session_state.history:
            prev_state = st.session_state.history.pop()
            
            # Khôi phục drivers
            driver_manager = st.session_state.driver_manager
            driver_manager.drivers = []
            driver_manager.id_index = {}
            for d in prev_state['drivers']:
                driver = Driver(
                    d['ID'], 
                    d['Ten'], 
                    d['Rating'], 
                    d['X'], 
                    d['Y'],
                    d.get('Trips', 0),
                    d.get('Experience', 0)
                )
                driver_manager.drivers.append(driver)
                driver_manager.id_index[driver.id] = driver
            
            # Khôi phục customers
            customer_manager = st.session_state.customer_manager
            customer_manager.customers = {}
            for cid, c in prev_state['customers'].items():
                customer = Customer(c['ID'], c['Ten'], c['Quan'], c['X'], c['Y'])
                customer_manager.customers[customer.id] = customer
            
            # Khôi phục rides
            ride_manager = st.session_state.ride_manager
            ride_manager.rides = []
            ride_manager.driver_rides = {}
            for r in prev_state['rides']:
                ride = Ride(
                    r['RideID'],
                    r['CustomerID'],
                    r['DriverID'],
                    r['Distance'],
                    r['Fare'],
                    datetime.strptime(r['StartTime'], '%Y-%m-%d %H:%M:%S'),
                    datetime.strptime(r['EndTime'], '%Y-%m-%d %H:%M:%S'),
                    r['StartPoint'],
                    r['EndPoint']
                )
                ride_manager.rides.append(ride)
                if ride.driver_id not in ride_manager.driver_rides:
                    ride_manager.driver_rides[ride.driver_id] = []
                ride_manager.driver_rides[ride.driver_id].append(ride)
            
            st.success("Da hoan tac thao tac")
            return True
        else:
            st.warning("Khong co thao tac nao de hoan tac")
            return False


# MAIN APP
st.set_page_config(
    page_title="MinRide - Hệ thống Quản lý Đặt Xe",
    layout="wide"
)

st.title("Hệ thống Quản lý Đặt Xe Công Nghệ MinRide")

# KHỞI TẠO SESSION STATE 

# Khởi tạo session state manager
session_state_manager = ManageSessionState()
driver_manager = session_state_manager.get_driver_manager()
customer_manager = session_state_manager.get_customer_manager()
ride_manager = session_state_manager.get_ride_manager()

# Khởi tạo FindDriverSystem
if 'find_driver_system' not in st.session_state:
    st.session_state.find_driver_system = FindDriverSystem(driver_manager, customer_manager)
find_driver_system = st.session_state.find_driver_system

# Khởi tạo BookingSystem
if 'booking_system' not in st.session_state:
    st.session_state.booking_system = BookingSystem(driver_manager, customer_manager, ride_manager)
booking_system = st.session_state.booking_system

# Khởi tạo AutoMatchingSystem
if 'auto_matching_system' not in st.session_state:
    st.session_state.auto_matching_system = AutoMatchingSystem(
        driver_manager, customer_manager, booking_system
    )
auto_matching_system = st.session_state.auto_matching_system


# SIDEBAR 
st.sidebar.header("⚙️ Quan ly He thong")

# Nút Hoàn tác
if st.sidebar.button("↩️ Hoan tac", use_container_width=True):
    session_state_manager.undo()

st.sidebar.write("---")

# Nút Lưu file
st.sidebar.subheader("💾 Luu du lieu")
col1, col2, col3 = st.sidebar.columns(3)

with col1:
    if st.button("Drivers", use_container_width=True):
        driver_manager.save_to_file("drivers.csv")

with col2:
    if st.button("Customers", use_container_width=True):
        customer_manager.save_to_file("customers.csv")

with col3:
    if st.button("Rides", use_container_width=True):
        ride_manager.save_to_file("rides.csv")

st.sidebar.write("---")

# Thống kê hệ thống
st.sidebar.subheader("Thống kê")
st.sidebar.metric("Tai xe", len(driver_manager.drivers))
st.sidebar.metric("Khach hang", len(customer_manager.customers))
st.sidebar.metric("Chuyen di", len(ride_manager.rides))
st.sidebar.metric("Booking cho", len(booking_system.get_pending_bookings()))

# Hiển thị lịch sử undo
st.sidebar.write("---")
st.sidebar.subheader("Lịch sử")
history_count = len(st.session_state.history)
st.sidebar.write(f"Co the hoan tac: {history_count} buoc")


# ==================== MAIN TABS ====================

# Tạo các tab chính
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Quản lý tài xế", 
    "Quản lý khách hàng", 
    "Lịch sử chuyến đi", 
    "Tìm tài xế", 
    "Ghép cặp tự động"
])
