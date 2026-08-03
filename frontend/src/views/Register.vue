<template>
  <div class="min-h-screen flex">

    <!-- ── Left: Photo panel ── -->
    <div class="hidden lg:flex lg:w-1/2 relative overflow-hidden">
      <img
        src="https://images.unsplash.com/photo-1551632811-561732d1e306?w=1200&q=80"
        alt="Begin your adventure"
        class="absolute inset-0 w-full h-full object-cover"
      />
      <div class="absolute inset-0 bg-gradient-to-br from-green-900/75 via-slate-900/60 to-black/70"></div>

      <div class="relative z-10 flex flex-col justify-between p-10 w-full">
        <!-- Logo -->
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-green-500 rounded-xl flex items-center justify-center shadow-lg">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 17l5-10 4 8 3-5 4 7H3z"/>
            </svg>
          </div>
          <span class="text-white font-bold text-xl font-['Poppins']">Trek<span class="text-green-400">Hub</span></span>
        </div>

        <!-- Headline -->
        <div class="space-y-4">
          <h1 class="text-white text-5xl font-black font-['Poppins'] leading-tight">
            Begin Your<br><span class="text-green-400">Adventure.</span>
          </h1>
          <p class="text-slate-300 text-base leading-relaxed max-w-xs">
            Create your account and explore the most amazing trekking destinations with <span class="text-green-400 font-semibold">TrekHub</span>.
          </p>

          <!-- Perks -->
          <div class="space-y-3 pt-2">
            <div v-for="p in perks" :key="p.text" class="flex items-center gap-3">
              <div class="w-8 h-8 bg-green-500/20 border border-green-400/30 rounded-lg flex items-center justify-center text-sm flex-shrink-0">
                {{ p.icon }}
              </div>
              <span class="text-slate-300 text-sm">{{ p.text }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ── Right: Form panel ── -->
    <div class="flex-1 flex flex-col bg-white">
      <!-- Top bar -->
      <div class="flex justify-between items-center px-8 py-5">
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
      <div class="flex-1 flex items-center justify-center px-8 py-4">
        <div class="w-full max-w-lg space-y-6">
          <!-- Header -->
          <div class="text-center space-y-1">
            <h2 class="text-3xl font-bold text-gray-900 font-['Poppins']">Create Your Account</h2>
            <div class="w-10 h-1 bg-green-600 rounded-full mx-auto"></div>
            <p class="text-gray-500 text-sm mt-2">Join TrekHub and start your trekking journey today.</p>
          </div>

          <!-- Error alert -->
          <div v-if="error" class="flex items-center gap-2 bg-red-50 border border-red-200 text-red-700 rounded-xl px-4 py-3 text-sm">
            <svg class="w-4 h-4 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
            </svg>
            {{ error }}
          </div>

          <form @submit.prevent="handleRegister" class="space-y-4">
            <!-- Row: Name + Email -->
            <div class="grid grid-cols-2 gap-4">
              <div class="space-y-1.5">
                <label class="text-sm font-semibold text-gray-700">Full Name</label>
                <div class="relative">
                  <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                    <svg class="w-4 h-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                    </svg>
                  </div>
                  <input type="text" v-model="name" required placeholder="Enter your full name"
                    class="w-full pl-10 pr-4 py-3 border border-gray-200 rounded-xl text-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all bg-gray-50 focus:bg-white"/>
                </div>
              </div>
              <div class="space-y-1.5">
                <label class="text-sm font-semibold text-gray-700">Email Address</label>
                <div class="relative">
                  <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                    <svg class="w-4 h-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                    </svg>
                  </div>
                  <input type="email" v-model="email" required placeholder="Enter your email"
                    class="w-full pl-10 pr-4 py-3 border border-gray-200 rounded-xl text-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all bg-gray-50 focus:bg-white"/>
                </div>
              </div>
            </div>

            <!-- Row: Phone + DOB (visual only) -->
            <div class="grid grid-cols-2 gap-4">
              <div class="space-y-1.5">
                <label class="text-sm font-semibold text-gray-700">Phone Number</label>
                <div class="relative">
                  <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                    <svg class="w-4 h-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
                    </svg>
                  </div>
                  <input type="text" v-model="phone" placeholder="Enter your phone number"
                    class="w-full pl-10 pr-4 py-3 border border-gray-200 rounded-xl text-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all bg-gray-50 focus:bg-white"/>
                </div>
              </div>
              <div class="space-y-1.5">
                <label class="text-sm font-semibold text-gray-700">Date of Birth</label>
                <div class="relative">
                  <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                    <svg class="w-4 h-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <rect x="3" y="4" width="18" height="18" rx="2" ry="2" stroke-width="2"/>
                      <line x1="16" y1="2" x2="16" y2="6" stroke-width="2" stroke-linecap="round"/>
                      <line x1="8" y1="2" x2="8" y2="6" stroke-width="2" stroke-linecap="round"/>
                      <line x1="3" y1="10" x2="21" y2="10" stroke-width="2"/>
                    </svg>
                  </div>
                  <input type="date" v-model="dob"
                    class="w-full pl-10 pr-4 py-3 border border-gray-200 rounded-xl text-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all bg-gray-50 focus:bg-white"/>
                </div>
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
                <input :type="showPassword ? 'text' : 'password'" v-model="password" required placeholder="Create a password"
                  class="w-full pl-10 pr-10 py-3 border border-gray-200 rounded-xl text-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all bg-gray-50 focus:bg-white"/>
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
              <!-- Strength bar -->
              <div v-if="password.length > 0" class="flex items-center gap-2 mt-1">
                <div class="flex-1 h-1 rounded-full bg-gray-200 overflow-hidden">
                  <div class="h-full rounded-full transition-all duration-300"
                    :class="strengthBarClass"
                    :style="{ width: strengthPct + '%' }"></div>
                </div>
                <span class="text-xs font-medium" :class="strengthTextClass">{{ strengthLabel }}</span>
              </div>
            </div>

            <!-- Confirm Password -->
            <div class="space-y-1.5">
              <label class="text-sm font-semibold text-gray-700">Confirm Password</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                  <svg class="w-4 h-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2" stroke-width="2"/>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 11V7a5 5 0 0110 0v4"/>
                  </svg>
                </div>
                <input :type="showConfirm ? 'text' : 'password'" v-model="confirmPassword" required placeholder="Confirm your password"
                  class="w-full pl-10 pr-10 py-3 border border-gray-200 rounded-xl text-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all bg-gray-50 focus:bg-white"
                  :class="{ 'border-red-400 focus:ring-red-400': confirmPassword && password !== confirmPassword }"/>
                <button type="button" @click="showConfirm = !showConfirm"
                  class="absolute inset-y-0 right-0 pr-3.5 flex items-center text-gray-400 hover:text-gray-600">
                  <svg v-if="showConfirm" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"/>
                  </svg>
                  <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                  </svg>
                </button>
              </div>
              <p v-if="confirmPassword && password !== confirmPassword" class="text-xs text-red-500 mt-1">Passwords do not match</p>
            </div>

            <!-- Terms checkbox -->
            <label class="flex items-start gap-2.5 cursor-pointer">
              <input type="checkbox" v-model="agreed" required class="mt-0.5 w-4 h-4 rounded border-gray-300 text-green-600 focus:ring-green-500 flex-shrink-0"/>
              <span class="text-sm text-gray-600">
                I agree to the <a href="#" class="text-green-600 font-semibold hover:underline">Terms &amp; Conditions</a> and <a href="#" class="text-green-600 font-semibold hover:underline">Privacy Policy</a>
              </span>
            </label>

            <!-- Submit -->
            <button
              type="submit"
              :disabled="loading || (confirmPassword && password !== confirmPassword)"
              class="w-full flex items-center justify-center gap-2 bg-green-700 hover:bg-green-800 disabled:bg-green-400 text-white font-semibold py-3.5 rounded-xl transition-all duration-200 shadow-md hover:shadow-lg active:scale-[0.98] text-sm"
            >
              <svg v-if="loading" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
              </svg>
              <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/>
              </svg>
              {{ loading ? 'Creating account…' : 'Create Account' }}
            </button>

            <!-- Divider -->
            <div class="flex items-center gap-3">
              <div class="flex-1 h-px bg-gray-200"></div>
              <span class="text-gray-400 text-xs uppercase tracking-wide">OR</span>
              <div class="flex-1 h-px bg-gray-200"></div>
            </div>

            <p class="text-center text-sm text-gray-500">
              Already have an account?
              <router-link :to="{ name: 'Login' }" class="text-green-600 font-semibold hover:text-green-700 transition-colors">Login here</router-link>
            </p>
          </form>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import api from '../services/api';

export default {
  setup() {
    const router = useRouter();
    const name = ref('');
    const email = ref('');
    const phone = ref('');
    const dob = ref('');
    const password = ref('');
    const confirmPassword = ref('');
    const loading = ref(false);
    const error = ref('');
    const showPassword = ref(false);
    const showConfirm = ref(false);
    const agreed = ref(false);

    const perks = [
      { icon: '🗺', text: 'Browse 120+ curated trek routes' },
      { icon: '📅', text: 'Easy online booking & management' },
      { icon: '🔔', text: 'Real-time booking status alerts' },
      { icon: '🏅', text: 'Track your adventure history' },
    ];

    const strengthPct = computed(() => {
      const p = password.value;
      if (!p) return 0;
      let s = 0;
      if (p.length >= 6)  s += 25;
      if (p.length >= 10) s += 25;
      if (/[A-Z]/.test(p)) s += 25;
      if (/[^a-zA-Z0-9]/.test(p)) s += 25;
      return s;
    });

    const strengthLabel = computed(() => {
      const s = strengthPct.value;
      if (s <= 25) return 'Weak';
      if (s <= 50) return 'Fair';
      if (s <= 75) return 'Good';
      return 'Strong';
    });

    const strengthBarClass = computed(() => {
      const s = strengthPct.value;
      if (s <= 25) return 'bg-red-500';
      if (s <= 50) return 'bg-yellow-500';
      if (s <= 75) return 'bg-green-400';
      return 'bg-green-600';
    });

    const strengthTextClass = computed(() => {
      const s = strengthPct.value;
      if (s <= 25) return 'text-red-500';
      if (s <= 50) return 'text-yellow-600';
      if (s <= 75) return 'text-green-500';
      return 'text-green-600';
    });

    const handleRegister = async () => {
      if (password.value !== confirmPassword.value) return;
      loading.value = true;
      error.value = '';
      try {
        await api.post('/api/auth/register', {
          name: name.value,
          email: email.value,
          phone: phone.value,
          password: password.value
        });
        window.triggerToast('Registration successful! Please login.', 'success');
        router.push({ name: 'Login' });
      } catch (err) {
        error.value = err.response?.data?.error || 'Registration failed. Try again.';
        window.triggerToast(error.value, 'error');
      } finally {
        loading.value = false;
      }
    };

    return { name, email, phone, dob, password, confirmPassword, loading, error, showPassword, showConfirm, agreed, perks, strengthPct, strengthLabel, strengthBarClass, strengthTextClass, handleRegister };
  }
};
</script>
