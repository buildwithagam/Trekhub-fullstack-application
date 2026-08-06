<template>
  <div class="min-h-screen flex">

    <!-- ── Left: Photo panel ── -->
    <div class="hidden lg:flex lg:w-1/2 relative overflow-hidden">
      <!-- Real mountain photo via Unsplash -->
      <img
        src="https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1200&q=80"
        alt="Mountain trek"
        class="absolute inset-0 w-full h-full object-cover"
      />
      <!-- Dark gradient overlay -->
      <div class="absolute inset-0 bg-gradient-to-br from-green-900/80 via-slate-900/60 to-black/70"></div>

      <!-- Floating content -->
      <div class="relative z-10 flex flex-col justify-between p-10 w-full">
        <!-- Logo -->
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-green-500 rounded-xl flex items-center justify-center shadow-lg">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M3 17l5-10 4 8 3-5 4 7H3z"/>
            </svg>
          </div>
          <span class="text-white font-bold text-xl font-['Poppins']">Trek<span class="text-green-400">Hub</span></span>
        </div>

        <!-- Headline -->
        <div class="space-y-4">
          <div class="space-y-1">
            <h1 class="text-white text-5xl font-black font-['Poppins'] leading-tight">
              Explore.<br>Trek.<br>
              <span class="text-green-400">Create Memories.</span>
            </h1>
          </div>
          <p class="text-slate-300 text-base leading-relaxed max-w-xs">
            Discover the best trekking destinations, book your adventures and make unforgettable memories.
          </p>

          <!-- Stats row -->
          <div class="flex gap-6 pt-2">
            <div>
              <p class="text-white font-bold text-2xl font-['Poppins']">120+</p>
              <p class="text-slate-400 text-xs uppercase tracking-wide">Treks Listed</p>
            </div>
            <div class="w-px bg-white/20"></div>
            <div>
              <p class="text-white font-bold text-2xl font-['Poppins']">5K+</p>
              <p class="text-slate-400 text-xs uppercase tracking-wide">Adventurers</p>
            </div>
            <div class="w-px bg-white/20"></div>
            <div>
              <p class="text-white font-bold text-2xl font-['Poppins']">98%</p>
              <p class="text-slate-400 text-xs uppercase tracking-wide">Satisfaction</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ── Right: Form panel ── -->
    <div class="flex-1 flex flex-col bg-white">
      <!-- Top bar -->
      <div class="flex justify-between items-center px-8 py-5">
        <!-- Mobile logo -->
        <div class="flex lg:hidden items-center gap-2">
          <div class="w-8 h-8 bg-green-600 rounded-lg flex items-center justify-center">
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 17l5-10 4 8 3-5 4 7H3z"/>
            </svg>
          </div>
          <span class="font-bold text-gray-900 font-['Poppins']">Trek<span class="text-green-600">Hub</span></span>
        </div>
        <div class="hidden lg:block"></div>
        <button class="flex items-center gap-1.5 text-sm text-gray-500 hover:text-green-600 transition-colors">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="10" stroke-width="2"/>
            <path stroke-linecap="round" stroke-width="2" d="M12 8v4m0 4h.01"/>
          </svg>
          Need Help?
        </button>
      </div>

      <!-- Form area -->
      <div class="flex-1 flex items-center justify-center px-8 py-6">
        <div class="w-full max-w-md space-y-7">
          <!-- Header -->
          <div class="text-center space-y-1">
            <h2 class="text-3xl font-bold text-gray-900 font-['Poppins']">Welcome Back!</h2>
            <div class="w-10 h-1 bg-green-600 rounded-full mx-auto"></div>
            <p class="text-gray-500 text-sm mt-2">Login to your TrekHub account</p>
          </div>

          <!-- Error alert -->
          <div v-if="error" class="flex items-center gap-2 bg-red-50 border border-red-200 text-red-700 rounded-xl px-4 py-3 text-sm">
            <svg class="w-4 h-4 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
            </svg>
            {{ error }}
          </div>

          <!-- Form -->
          <form @submit.prevent="handleLogin" class="space-y-5">
            <!-- Email -->
            <div class="space-y-1.5">
              <label class="text-sm font-semibold text-gray-700">Email</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                  <svg class="w-4 h-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                  </svg>
                </div>
                <input
                  type="email"
                  v-model="email"
                  required
                  placeholder="Enter your email"
                  class="w-full pl-10 pr-4 py-3 border border-gray-200 rounded-xl text-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all bg-gray-50 focus:bg-white"
                />
              </div>
            </div>

            <!-- Password -->
            <div class="space-y-1.5">
              <label class="text-sm font-semibold text-gray-700">Password</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                  <svg class="w-4 h-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2" stroke-width="2"/>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 11V7a5 5 0 0110 0v4"/>
                  </svg>
                </div>
                <input
                  :type="showPassword ? 'text' : 'password'"
                  v-model="password"
                  required
                  placeholder="Enter your password"
                  class="w-full pl-10 pr-10 py-3 border border-gray-200 rounded-xl text-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all bg-gray-50 focus:bg-white"
                />
                <button type="button" @click="showPassword = !showPassword"
                  class="absolute inset-y-0 right-0 pr-3.5 flex items-center text-gray-400 hover:text-gray-600">
                  <svg v-if="showPassword" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"/>
                  </svg>
                  <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                  </svg>
                </button>
              </div>
            </div>

            <!-- Remember + Forgot -->
            <div class="flex items-center justify-between text-sm">
              <label class="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" class="w-4 h-4 rounded border-gray-300 text-green-600 focus:ring-green-500"/>
                <span class="text-gray-600">Remember me</span>
              </label>
              <a href="#" class="text-green-600 font-semibold hover:text-green-700 transition-colors">Forgot Password?</a>
            </div>

            <!-- Submit -->
            <button
              type="submit"
              :disabled="loading"
              class="w-full flex items-center justify-center gap-2 bg-green-700 hover:bg-green-800 disabled:bg-green-400 text-white font-semibold py-3.5 rounded-xl transition-all duration-200 shadow-md hover:shadow-lg active:scale-[0.98] text-sm"
            >
              <svg v-if="loading" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
              </svg>
              <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1"/>
              </svg>
              {{ loading ? 'Signing in…' : 'Login' }}
            </button>

            <!-- Divider -->
            <div class="flex items-center gap-3">
              <div class="flex-1 h-px bg-gray-200"></div>
              <span class="text-gray-400 text-xs uppercase tracking-wide">OR</span>
              <div class="flex-1 h-px bg-gray-200"></div>
            </div>

            <!-- Demo credentials dropdown -->
            <div class="relative">
              <button type="button" @click="showDemoPanel = !showDemoPanel"
                class="w-full flex items-center justify-between gap-2 border border-gray-200 text-gray-600 hover:bg-gray-50 font-medium py-2.5 px-4 rounded-xl transition-all text-sm">
                <span class="flex items-center gap-2">
                  <span class="text-base">🔑</span>
                  Demo Credentials
                </span>
                <svg class="w-4 h-4 text-gray-400 transition-transform duration-200" :class="showDemoPanel ? 'rotate-180' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                </svg>
              </button>

              <!-- Panel -->
              <div v-if="showDemoPanel"
                class="absolute bottom-full mb-2 left-0 right-0 bg-white border border-gray-200 rounded-2xl shadow-xl overflow-hidden z-10">
                <div class="px-4 py-2.5 bg-gray-50 border-b border-gray-100">
                  <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide">Click to auto-fill</p>
                </div>
                <div class="divide-y divide-gray-50">
                  <button v-for="cred in demoCreds" :key="cred.role" type="button"
                    @click="fillCredentials(cred)"
                    class="w-full flex items-center gap-3 px-4 py-3 hover:bg-green-50 transition-colors text-left group">
                    <span class="w-8 h-8 rounded-xl flex items-center justify-center text-base shrink-0" :class="cred.bg">{{ cred.icon }}</span>
                    <div class="flex-1 min-w-0">
                      <p class="text-sm font-semibold text-gray-900 group-hover:text-green-700">{{ cred.role }}</p>
                      <p class="text-xs text-gray-400">{{ cred.email }}</p>
                    </div>
                    <span class="text-xs text-gray-300 group-hover:text-green-500 font-mono">pass123</span>
                  </button>
                </div>
              </div>
            </div>
          </form>

          <!-- Register link -->
          <p class="text-center text-sm text-gray-500">
            Don't have an account?
            <router-link :to="{ name: 'Register' }" class="text-green-600 font-semibold hover:text-green-700 transition-colors">Register here</router-link>
          </p>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '../services/api';
import store from '../store';

export default {
  setup() {
    const router = useRouter();
    const email = ref('');
    const password = ref('');
    const loading = ref(false);
    const error = ref('');
    const showPassword = ref(false);
    const showDemoPanel = ref(false);

    const demoCreds = [
      { role: 'Trekker', email: 'trekker@tma.com', password: 'pass123', icon: '🥾', bg: 'bg-green-100' },
      { role: 'Staff',   email: 'staff@tma.com',   password: 'pass123', icon: '🧑‍💼', bg: 'bg-orange-100' },
      { role: 'Admin',   email: 'admin@tma.com',   password: 'pass123', icon: '🛡',  bg: 'bg-red-100' },
    ];

    const fillCredentials = (cred) => {
      email.value = cred.email;
      password.value = cred.password;
      showDemoPanel.value = false;
    };

    const handleLogin = async () => {
      loading.value = true;
      error.value = '';
      try {
        const res = await api.post('/api/auth/login', {
          email: email.value,
          password: password.value
        });

        const { user, access_token, refresh_token } = res.data;
        store.login(user, access_token, refresh_token);
        window.triggerToast('Welcome back, ' + user.name + '!', 'success');

        if (user.role === 'ADMIN') router.push({ name: 'AdminDashboard' });
        else if (user.role === 'STAFF') router.push({ name: 'StaffDashboard' });
        else router.push({ name: 'TrekkerDashboard' });
      } catch (err) {
        error.value = err.response?.data?.error || 'Failed to authenticate. Please check your credentials.';
        window.triggerToast(error.value, 'error');
      } finally {
        loading.value = false;
      }
    };

    return { email, password, loading, error, showPassword, showDemoPanel, demoCreds, fillCredentials, handleLogin };
  }
};
</script>
