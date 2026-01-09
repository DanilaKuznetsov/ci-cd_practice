const API_BASE_URL = 'http://localhost:5000/api';

class API {
  async request(endpoint, method = 'GET', data = null) {
    const url = new URL(`${API_BASE_URL}${endpoint}`);
    const options = {
      method: method,
      headers: {
        'Content-Type': 'application/json'
      }
    };
    
    if (data && (method === 'POST' || method === 'PUT')) {
      options.body = JSON.stringify(data);
    }
    
    try {
      const response = await fetch(url, options);
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Ошибка запроса');
      }
      return await response.json();
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  }

  async getCourses() {
    return await this.request('/courses');
  }

  async getCourse(id) {
    return await this.request(`/courses/${id}`);
  }

  async getTutors() {
    return await this.request('/tutors');
  }

  async getTutor(id) {
    return await this.request(`/tutors/${id}`);
  }

  async getOrders() {
    return await this.request('/orders');
  }

  async getOrder(id) {
    return await this.request(`/orders/${id}`);
  }

  async createOrder(orderData) {
    return await this.request('/orders', 'POST', orderData);
  }

  async updateOrder(id, orderData) {
    return await this.request(`/orders/${id}`, 'PUT', orderData);
  }

  async deleteOrder(id) {
    return await this.request(`/orders/${id}`, 'DELETE');
  }
}

const api = new API();
