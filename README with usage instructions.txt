Vendor Management System API
This Vendor Management System API provides endpoints for managing vendors and purchase orders. It allows users to create, update, delete, and retrieve information about vendors and purchase orders.

The API will be accessible at http://localhost:8000/.

API Endpoints

Vendors
GET /api/vendors/: Retrieve a list of all vendors.
POST /api/vendors/: Create a new vendor.
GET /api/vendors/{vendor_id}/: Retrieve details of a specific vendor.
PUT /api/vendors/{vendor_id}/: Update information of a specific vendor.
DELETE /api/vendors/{vendor_id}/: Delete a specific vendor.

Purchase Orders
POST /api/purchase-orders/: Create a new purchase order.
GET /api/purchase-orders/: Retrieve a list of all purchase orders. Optionally filter by vendor using query parameter vendor.
GET /api/purchase-orders/{po_id}/: Retrieve details of a specific purchase order.
PUT /api/purchase-orders/{po_id}/: Update information of a specific purchase order.
DELETE /api/purchase-orders/{po_id}/: Delete a specific purchase order.

Vendor Performance
GET /api/vendors/{vendor_id}/performance/: Retrieve performance metrics of a specific vendor.

Usage

1. Vendor Management:
Create Vendor:
To create a new vendor, send a POST request to /api/vendors/ with the necessary details in the request body, such as name, contact details, address, and vendor code.

Retrieve Vendor List:
To retrieve a list of all vendors, send a GET request to /api/vendors/. This endpoint will return a JSON response containing details of all the vendors.

Retrieve Vendor Details:
To retrieve details of a specific vendor, send a GET request to /api/vendors/{vendor_id}/, where {vendor_id} is the unique identifier of the vendor.

Update Vendor:
To update information of a specific vendor, send a PUT request to /api/vendors/{vendor_id}/ with the updated details in the request body.

Delete Vendor:
To delete a specific vendor, send a DELETE request to /api/vendors/{vendor_id}/. This will remove the vendor from the system.

2. Purchase Order Management:
Create Purchase Order:
To create a new purchase order, send a POST request to /api/purchase-orders/ with the necessary details in the request body, such as PO number, vendor ID, order date, items, quantity, and optionally delivery date, status, and quality rating.

Retrieve Purchase Order List:
To retrieve a list of all purchase orders, send a GET request to /api/purchase-orders/. Optionally, you can filter the purchase orders by vendor using the query parameter vendor.

Retrieve Purchase Order Details:
To retrieve details of a specific purchase order, send a GET request to /api/purchase-orders/{po_id}/, where {po_id} is the unique identifier of the purchase order.

Update Purchase Order:
To update information of a specific purchase order, send a PUT request to /api/purchase-orders/{po_id}/ with the updated details in the request body.

Delete Purchase Order:
To delete a specific purchase order, send a DELETE request to /api/purchase-orders/{po_id}/. This will remove the purchase order from the system.

3. Vendor Performance Metrics:
Retrieve Vendor Performance Metrics:
To retrieve performance metrics of a specific vendor, send a GET request to /api/vendors/{vendor_id}/performance/. This endpoint will return metrics such as on-time delivery rate, quality rating average, average response time, and fulfillment rate.

Sample Requests:
Refer to the README file for sample requests using cURL for some of the endpoints.

Feel free to reach out if you need further clarification on any specific endpoint or functionality!