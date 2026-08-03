<template>
  <div class="flex h-screen bg-gray-50 overflow-hidden" style="font-family:'Inter',sans-serif;">

    <!-- ══ SIDEBAR ══ -->
    <aside class="hidden lg:flex flex-col w-60 shrink-0 bg-slate-900 text-white overflow-hidden">
      <!-- Logo -->
      <div class="flex items-center gap-3 px-5 py-5 border-b border-slate-800">
        <div class="w-9 h-9 bg-green-600 rounded-xl flex items-center justify-center shadow">
          <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M3 17l5-10 4 8 3-5 4 7H3z"/>
          </svg>
        </div>
        <span class="font-bold text-lg" style="font-family:'Poppins',sans-serif">Trek<span class="text-green-400">Hub</span></span>
        <span class="ml-auto text-xs font-bold bg-red-500/20 text-red-400 border border-red-500/30 px-2 py-0.5 rounded-full">Admin</span>
      </div>

      <!-- Nav -->
      <nav class="flex-1 py-4 px-3 space-y-0.5">
        <button v-for="item in navItems" :key="item.key"
          @click="activeTab = item.key"
          class="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all text-left"
          :class="activeTab === item.key ? 'bg-green-700 text-white' : 'text-slate-400 hover:bg-slate-800 hover:text-white'">
          <span class="text-base">{{ item.icon }}</span>
          {{ item.label }}
        </button>
      </nav>

      <!-- Banner image -->
      <div class="mx-3 mb-3 rounded-2xl overflow-hidden relative h-32">
        <img src="https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=400&q=70"
          class="w-full h-full object-cover"/>
        <div class="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent flex items-end p-3">
          <p class="text-white text-xs font-semibold">Manage every expedition</p>
        </div>
      </div>

      <!-- Logout -->
      <div class="px-3 pb-4">
        <button @click="handleLogout"
          class="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium text-red-400 hover:bg-red-500/10 hover:text-red-300 transition-all">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
          </svg>
          Logout
        </button>
      </div>
    </aside>

    <!-- ══ MAIN ══ -->
    <div class="flex-1 flex flex-col min-w-0 overflow-hidden">

      <!-- Top bar -->
      <header class="flex items-center px-6 py-3.5 bg-white border-b border-gray-100 shrink-0 shadow-sm">
        <div>
          <h2 class="text-gray-800 font-semibold text-sm">{{ currentPageTitle }}</h2>
        </div>
        <div class="flex items-center gap-3 ml-auto">
          <div class="flex items-center gap-2.5 pl-3 border-l border-gray-200">
            <div class="w-8 h-8 rounded-full bg-red-600 flex items-center justify-center text-white font-bold text-sm shadow">
              {{ (user?.name || 'A').charAt(0).toUpperCase() }}
            </div>
            <div class="hidden sm:block leading-tight">
              <p class="text-sm font-semibold text-gray-900">{{ user?.name }}</p>
              <p class="text-xs text-red-500 font-semibold">Administrator</p>
            </div>
          </div>
          <button @click="handleLogout"
            class="flex items-center gap-1.5 text-xs font-semibold text-red-500 border border-red-200 hover:bg-red-50 px-3 py-1.5 rounded-lg transition-all">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7"/>
            </svg>
            Sign out
          </button>
        </div>
      </header>

      <main class="flex-1 overflow-y-auto p-6">

        <!-- ── OVERVIEW (metrics) ── -->
        <div v-show="activeTab === 'overview'" class="space-y-6">
          <!-- Hero banner -->
          <div class="relative rounded-2xl overflow-hidden h-40">
            <img src="https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1200&q=70"
              class="w-full h-full object-cover"/>
            <div class="absolute inset-0 bg-gradient-to-r from-slate-900/80 to-transparent flex items-center px-8">
              <div>
                <h1 class="text-white text-2xl font-black" style="font-family:'Poppins',sans-serif">Admin Console</h1>
                <p class="text-slate-300 text-sm mt-1">Manage staff, treks, users and analytics</p>
              </div>
            </div>
          </div>

          <!-- Metric cards -->
          <div class="grid grid-cols-2 lg:grid-cols-3 gap-4">
            <div v-for="(val, label) in metrics" :key="label"
              class="bg-white rounded-2xl border border-gray-100 p-5 shadow-sm hover:shadow-md transition-shadow">
              <p class="text-xs text-gray-400 font-semibold uppercase tracking-wide">{{ formatLabel(label) }}</p>
              <p class="text-3xl font-black text-gray-900 mt-1" style="font-family:'Poppins',sans-serif">{{ val }}</p>
            </div>
          </div>

          <!-- Quick nav cards -->
          <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
            <button v-for="qn in quickNav" :key="qn.tab" @click="activeTab = qn.tab"
              class="bg-white rounded-2xl border border-gray-100 p-4 shadow-sm hover:shadow-lg hover:-translate-y-1 transition-all text-left group overflow-hidden relative">
              <div class="relative h-20 -mx-4 -mt-4 mb-3 overflow-hidden rounded-t-2xl">
                <img :src="qn.img" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"/>
                <div class="absolute inset-0 bg-gradient-to-t from-black/40 to-transparent"></div>
              </div>
              <span class="text-xl">{{ qn.icon }}</span>
              <p class="font-bold text-gray-900 text-sm mt-1">{{ qn.label }}</p>
              <p class="text-xs text-gray-400 mt-0.5">{{ qn.sub }}</p>
            </button>
          </div>
        </div>

        <!-- ── STAFF TAB ── -->
        <div v-show="activeTab === 'staff'" class="space-y-5">
          <div class="flex items-center justify-between">
            <h1 class="text-xl font-bold text-gray-900" style="font-family:'Poppins',sans-serif">Trek Staff Guides</h1>
            <div class="flex items-center gap-3">
              <input type="text" v-model="staffSearchQuery" @input="fetchStaff" placeholder="Search staff..."
                class="px-3 py-2 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-green-500 bg-gray-50 w-48"/>
              <button @click="showStaffModal = true; resetStaffForm()"
                class="flex items-center gap-2 bg-green-700 hover:bg-green-800 text-white font-semibold px-4 py-2 rounded-xl text-sm transition-all shadow-sm">
                + Add Staff
              </button>
            </div>
          </div>
          <div class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
            <table class="w-full text-sm">
              <thead>
                <tr class="bg-gray-50 border-b border-gray-100">
                  <th class="text-left px-5 py-3.5 text-xs font-semibold text-gray-500 uppercase tracking-wide">Staff</th>
                  <th class="text-left px-5 py-3.5 text-xs font-semibold text-gray-500 uppercase tracking-wide hidden md:table-cell">Experience</th>
                  <th class="text-left px-5 py-3.5 text-xs font-semibold text-gray-500 uppercase tracking-wide hidden lg:table-cell">Certifications</th>
                  <th class="text-left px-5 py-3.5 text-xs font-semibold text-gray-500 uppercase tracking-wide">Status</th>
                  <th class="px-5 py-3.5 text-xs font-semibold text-gray-500 uppercase tracking-wide">Actions</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-50">
                <tr v-for="s in staffList" :key="s.id" class="hover:bg-gray-50 transition-colors">
                  <td class="px-5 py-3.5">
                    <div class="flex items-center gap-3">
                      <div class="w-9 h-9 rounded-xl bg-green-600 flex items-center justify-center text-white font-bold text-sm shrink-0">
                        {{ s.name.charAt(0).toUpperCase() }}
                      </div>
                      <div>
                        <p class="font-semibold text-gray-900">{{ s.name }}</p>
                        <p class="text-xs text-gray-400">{{ s.email }}</p>
                      </div>
                    </div>
                  </td>
                  <td class="px-5 py-3.5 text-gray-500 hidden md:table-cell">{{ s.experience }} yrs</td>
                  <td class="px-5 py-3.5 text-gray-400 text-xs hidden lg:table-cell max-w-xs truncate">{{ s.certifications || 'None' }}</td>
                  <td class="px-5 py-3.5">
                    <span class="inline-flex px-2.5 py-1 rounded-full text-xs font-semibold"
                      :class="s.is_blacklisted ? 'bg-red-100 text-red-600' : s.is_active ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-500'">
                      {{ s.is_blacklisted ? 'Blacklisted' : s.is_active ? 'Active' : 'Inactive' }}
                    </span>
                  </td>
                  <td class="px-5 py-3.5">
                    <div class="flex items-center gap-1.5 flex-wrap">
                      <button @click="editStaff(s); showStaffModal = true" class="text-xs font-semibold text-blue-600 border border-blue-200 hover:bg-blue-50 px-2.5 py-1 rounded-lg transition-all">Edit</button>
                      <button @click="toggleStaffBlacklist(s)" class="text-xs font-semibold text-yellow-600 border border-yellow-200 hover:bg-yellow-50 px-2.5 py-1 rounded-lg transition-all">
                        {{ s.is_blacklisted ? 'Unblock' : 'Blacklist' }}
                      </button>
                      <button @click="toggleStaffActive(s)" class="text-xs font-semibold text-gray-600 border border-gray-200 hover:bg-gray-50 px-2.5 py-1 rounded-lg transition-all">
                        {{ s.is_active ? 'Deactivate' : 'Activate' }}
                      </button>
                      <button @click="deleteStaff(s.id)" class="text-xs font-semibold text-red-500 border border-red-200 hover:bg-red-50 px-2.5 py-1 rounded-lg transition-all">Delete</button>
                    </div>
                  </td>
                </tr>
                <tr v-if="staffList.length === 0">
                  <td colspan="5" class="text-center py-16 text-gray-400"><span class="text-3xl block mb-2">👥</span>No staff found.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- ── TREKS TAB ── -->
        <div v-show="activeTab === 'treks'" class="space-y-5">
          <div class="flex items-center justify-between">
            <h1 class="text-xl font-bold text-gray-900" style="font-family:'Poppins',sans-serif">Trek Trails</h1>
            <div class="flex items-center gap-3">
              <input type="text" v-model="trekSearchQuery" @input="fetchTreks" placeholder="Search location..."
                class="px-3 py-2 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-green-500 bg-gray-50 w-48"/>
              <button @click="showTrekModal = true; resetTrekForm()"
                class="flex items-center gap-2 bg-green-700 hover:bg-green-800 text-white font-semibold px-4 py-2 rounded-xl text-sm transition-all shadow-sm">
                + Create Trek
              </button>
            </div>
          </div>

          <!-- Trek cards grid with images -->
          <div class="grid sm:grid-cols-2 xl:grid-cols-3 gap-5">
            <div v-for="t in treks" :key="t.id"
              class="bg-white rounded-2xl border border-gray-100 shadow-sm hover:shadow-lg hover:-translate-y-1 transition-all duration-200 overflow-hidden group">
              <div class="relative h-36 overflow-hidden">
                <img :src="getTrekImage(t.trek_name)" :alt="t.trek_name"
                  class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"/>
                <div class="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent"></div>
                <span class="absolute top-2.5 right-2.5 text-xs font-bold px-2.5 py-1 rounded-full"
                  :class="t.difficulty==='Easy' ? 'bg-green-500 text-white' : t.difficulty==='Moderate' ? 'bg-yellow-500 text-white' : 'bg-red-500 text-white'">
                  {{ t.difficulty }}
                </span>
                <span class="absolute bottom-2.5 left-2.5 text-white text-xs font-semibold">📍 {{ t.location }}</span>
              </div>
              <div class="p-4">
                <div class="flex items-start justify-between gap-2 mb-2">
                  <h3 class="font-bold text-gray-900 text-sm leading-tight">{{ t.trek_name }}</h3>
                  <span class="text-xs font-semibold px-2 py-0.5 rounded-full shrink-0"
                    :class="t.status==='Open' ? 'bg-green-100 text-green-700' : t.status==='Pending' ? 'bg-yellow-100 text-yellow-700' : t.status==='Completed' ? 'bg-blue-100 text-blue-700' : 'bg-gray-100 text-gray-500'">
                    {{ t.status }}
                  </span>
                </div>
                <div class="flex gap-3 text-xs text-gray-400 mb-3">
                  <span>📅 {{ formatDate(t.start_date) }}</span>
                  <span>🪑 {{ t.available_slots }}/{{ t.total_slots }} slots</span>
                </div>
                <div class="flex items-center gap-1.5 flex-wrap">
                  <button @click="editTrek(t); showTrekModal = true" class="text-xs font-semibold text-blue-600 border border-blue-200 hover:bg-blue-50 px-2.5 py-1 rounded-lg transition-all">Edit</button>
                  <button @click="updateTrekStatus(t.id, 'Approved')" v-if="t.status==='Pending'" class="text-xs font-semibold text-green-600 border border-green-200 hover:bg-green-50 px-2.5 py-1 rounded-lg transition-all">Approve</button>
                  <button @click="updateTrekStatus(t.id, 'Open')" v-if="t.status==='Approved'" class="text-xs font-semibold text-blue-600 border border-blue-200 hover:bg-blue-50 px-2.5 py-1 rounded-lg transition-all">Open</button>
                  <button @click="updateTrekStatus(t.id, 'Closed')" v-if="t.status==='Open'" class="text-xs font-semibold text-yellow-600 border border-yellow-200 hover:bg-yellow-50 px-2.5 py-1 rounded-lg transition-all">Close</button>
                  <button @click="updateTrekStatus(t.id, 'Completed')" v-if="t.status==='Open'||t.status==='Closed'" class="text-xs font-semibold text-purple-600 border border-purple-200 hover:bg-purple-50 px-2.5 py-1 rounded-lg transition-all">Complete</button>
                  <button @click="deleteTrek(t.id)" class="text-xs font-semibold text-red-500 border border-red-200 hover:bg-red-50 px-2.5 py-1 rounded-lg transition-all">Delete</button>
                </div>
              </div>
            </div>
            <div v-if="treks.length === 0" class="col-span-full text-center py-16 text-gray-400">
              <span class="text-4xl block mb-2">🏔</span>No treks found.
            </div>
          </div>
        </div>

        <!-- ── USERS TAB ── -->
        <div v-show="activeTab === 'users'" class="space-y-5">
          <div class="flex items-center justify-between">
            <h1 class="text-xl font-bold text-gray-900" style="font-family:'Poppins',sans-serif">Trekker Registry</h1>
            <input type="text" v-model="userSearchQuery" @input="fetchUsers" placeholder="Search name/email..."
              class="px-3 py-2 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-green-500 bg-gray-50 w-56"/>
          </div>
          <div class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
            <table class="w-full text-sm">
              <thead>
                <tr class="bg-gray-50 border-b border-gray-100">
                  <th class="text-left px-5 py-3.5 text-xs font-semibold text-gray-500 uppercase tracking-wide">User</th>
                  <th class="text-left px-5 py-3.5 text-xs font-semibold text-gray-500 uppercase tracking-wide hidden md:table-cell">Phone</th>
                  <th class="text-left px-5 py-3.5 text-xs font-semibold text-gray-500 uppercase tracking-wide hidden lg:table-cell">Registered</th>
                  <th class="text-left px-5 py-3.5 text-xs font-semibold text-gray-500 uppercase tracking-wide">Status</th>
                  <th class="px-5 py-3.5 text-xs font-semibold text-gray-500 uppercase tracking-wide">Actions</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-50">
                <tr v-for="u in usersList" :key="u.id" class="hover:bg-gray-50 transition-colors">
                  <td class="px-5 py-3.5">
                    <div class="flex items-center gap-3">
                      <div class="w-9 h-9 rounded-xl bg-blue-600 flex items-center justify-center text-white font-bold text-sm shrink-0">
                        {{ u.name.charAt(0).toUpperCase() }}
                      </div>
                      <div>
                        <p class="font-semibold text-gray-900">{{ u.name }}</p>
                        <p class="text-xs text-gray-400">{{ u.email }}</p>
                      </div>
                    </div>
                  </td>
                  <td class="px-5 py-3.5 text-gray-500 hidden md:table-cell">{{ u.phone || '—' }}</td>
                  <td class="px-5 py-3.5 text-gray-400 text-xs hidden lg:table-cell">{{ u.created_at }}</td>
                  <td class="px-5 py-3.5">
                    <span class="inline-flex px-2.5 py-1 rounded-full text-xs font-semibold"
                      :class="u.is_blacklisted ? 'bg-red-100 text-red-600' : u.is_active ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-500'">
                      {{ u.is_blacklisted ? 'Blacklisted' : u.is_active ? 'Active' : 'Inactive' }}
                    </span>
                  </td>
                  <td class="px-5 py-3.5">
                    <div class="flex items-center gap-1.5">
                      <button @click="toggleUserBlacklist(u)" class="text-xs font-semibold text-yellow-600 border border-yellow-200 hover:bg-yellow-50 px-2.5 py-1 rounded-lg transition-all">
                        {{ u.is_blacklisted ? 'Unblock' : 'Blacklist' }}
                      </button>
                      <button @click="toggleUserActive(u)" class="text-xs font-semibold text-gray-600 border border-gray-200 hover:bg-gray-50 px-2.5 py-1 rounded-lg transition-all">
                        {{ u.is_active ? 'Deactivate' : 'Activate' }}
                      </button>
                    </div>
                  </td>
                </tr>
                <tr v-if="usersList.length === 0">
                  <td colspan="5" class="text-center py-16 text-gray-400"><span class="text-3xl block mb-2">👤</span>No users found.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- ── BOOKINGS TAB ── -->
        <div v-show="activeTab === 'bookings'" class="space-y-5">
          <div class="flex items-center justify-between">
            <h1 class="text-xl font-bold text-gray-900" style="font-family:'Poppins',sans-serif">Bookings Log</h1>
            <input type="text" v-model="bookingSearchQuery" @input="fetchBookings" placeholder="Search user/trek..."
              class="px-3 py-2 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-green-500 bg-gray-50 w-56"/>
          </div>
          <div class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
            <table class="w-full text-sm">
              <thead>
                <tr class="bg-gray-50 border-b border-gray-100">
                  <th class="text-left px-5 py-3.5 text-xs font-semibold text-gray-500 uppercase tracking-wide">User</th>
                  <th class="text-left px-5 py-3.5 text-xs font-semibold text-gray-500 uppercase tracking-wide">Trek</th>
                  <th class="text-left px-5 py-3.5 text-xs font-semibold text-gray-500 uppercase tracking-wide hidden md:table-cell">Booked On</th>
                  <th class="text-left px-5 py-3.5 text-xs font-semibold text-gray-500 uppercase tracking-wide">Status</th>
                  <th class="text-left px-5 py-3.5 text-xs font-semibold text-gray-500 uppercase tracking-wide hidden lg:table-cell">Payment</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-50">
                <tr v-for="b in bookingsList" :key="b.id" class="hover:bg-gray-50 transition-colors">
                  <td class="px-5 py-3.5">
                    <p class="font-semibold text-gray-900">{{ b.user_name }}</p>
                    <p class="text-xs text-gray-400">{{ b.user_email }}</p>
                  </td>
                  <td class="px-5 py-3.5">
                    <p class="font-semibold text-gray-900">{{ b.trek_name }}</p>
                    <p class="text-xs text-gray-400">{{ b.location }}</p>
                  </td>
                  <td class="px-5 py-3.5 text-gray-400 text-xs hidden md:table-cell">{{ b.booking_date }}</td>
                  <td class="px-5 py-3.5">
                    <span class="inline-flex px-2.5 py-1 rounded-full text-xs font-semibold"
                      :class="b.booking_status==='Booked' ? 'bg-green-100 text-green-700' : b.booking_status==='Completed' ? 'bg-blue-100 text-blue-700' : 'bg-red-100 text-red-600'">
                      {{ b.booking_status }}
                    </span>
                  </td>
                  <td class="px-5 py-3.5 hidden lg:table-cell">
                    <span class="inline-flex px-2.5 py-1 rounded-full text-xs font-semibold"
                      :class="b.payment_status==='Paid' ? 'bg-green-100 text-green-700' : b.payment_status==='Pending' ? 'bg-yellow-100 text-yellow-700' : 'bg-red-100 text-red-600'">
                      {{ b.payment_status }}
                    </span>
                  </td>
                </tr>
                <tr v-if="bookingsList.length === 0">
                  <td colspan="5" class="text-center py-16 text-gray-400"><span class="text-3xl block mb-2">📋</span>No bookings found.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- ── REPORTS TAB ── -->
        <div v-show="activeTab === 'reports'" class="space-y-5">
          <h1 class="text-xl font-bold text-gray-900" style="font-family:'Poppins',sans-serif">Reports & Analytics</h1>
          <div class="grid lg:grid-cols-3 gap-5">
            <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-5">
              <h3 class="font-bold text-gray-700 text-sm mb-3">Trails by Difficulty</h3>
              <div class="relative" style="height:180px"><canvas id="difficultyChart"></canvas></div>
            </div>
            <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-5">
              <h3 class="font-bold text-gray-700 text-sm mb-3">Bookings by Status</h3>
              <div class="relative" style="height:180px"><canvas id="bookingsChart"></canvas></div>
            </div>
            <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-5">
              <h3 class="font-bold text-gray-700 text-sm mb-3">Monthly Volume</h3>
              <div class="relative" style="height:180px"><canvas id="monthlyBookingsChart"></canvas></div>
            </div>
          </div>
          <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-6 text-center">
            <div class="text-4xl mb-3">📊</div>
            <h3 class="font-bold text-gray-900 text-base mb-1">Generate Monthly Summary Report</h3>
            <p class="text-gray-500 text-sm mb-4">Creates an HTML report outlining treks, bookings, and metrics.</p>
            <button @click="triggerMonthlyReport"
              class="inline-flex items-center gap-2 border border-green-600 text-green-700 hover:bg-green-50 font-semibold px-5 py-2.5 rounded-xl text-sm transition-all">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
              Trigger HTML Report
            </button>
          </div>
        </div>

      </main>
    </div>

    <!-- ══ STAFF MODAL ══ -->
    <div v-if="showStaffModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4" @click.self="showStaffModal = false">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md modal-animate overflow-y-auto max-h-[90vh]">
        <div class="flex items-center justify-between px-6 py-4 border-b border-gray-100">
          <h3 class="font-bold text-gray-900">{{ isEditingStaff ? 'Edit Staff' : 'Add Staff Guide' }}</h3>
          <button @click="showStaffModal = false" class="w-8 h-8 flex items-center justify-center rounded-xl hover:bg-gray-100 text-gray-400 transition-all">✕</button>
        </div>
        <form @submit.prevent="saveStaff()" class="p-6 space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div class="space-y-1.5">
              <label class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Full Name</label>
              <input type="text" v-model="staffForm.name" required class="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-green-500 bg-gray-50"/>
            </div>
            <div class="space-y-1.5">
              <label class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Email</label>
              <input type="email" v-model="staffForm.email" required :disabled="isEditingStaff" class="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-green-500 bg-gray-50 disabled:opacity-50"/>
            </div>
          </div>
          <div v-if="!isEditingStaff" class="space-y-1.5">
            <label class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Password</label>
            <input type="password" v-model="staffForm.password" required class="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-green-500 bg-gray-50"/>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div class="space-y-1.5">
              <label class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Phone</label>
              <input type="text" v-model="staffForm.phone" class="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-green-500 bg-gray-50"/>
            </div>
            <div class="space-y-1.5">
              <label class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Experience (yrs)</label>
              <input type="number" v-model="staffForm.experience" class="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-green-500 bg-gray-50"/>
            </div>
          </div>
          <div class="space-y-1.5">
            <label class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Certifications</label>
            <textarea v-model="staffForm.certifications" rows="2" class="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-green-500 bg-gray-50 resize-none"></textarea>
          </div>
          <div class="space-y-1.5">
            <label class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Emergency Contact</label>
            <input type="text" v-model="staffForm.emergency_contact" class="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-green-500 bg-gray-50"/>
          </div>
          <div class="flex gap-3 pt-2">
            <button type="button" @click="showStaffModal = false" class="flex-1 border border-gray-200 text-gray-600 font-semibold py-2.5 rounded-xl hover:bg-gray-50 text-sm transition-all">Cancel</button>
            <button type="submit" class="flex-1 bg-green-700 hover:bg-green-800 text-white font-semibold py-2.5 rounded-xl text-sm transition-all shadow-sm">Save</button>
          </div>
        </form>
      </div>
    </div>

    <!-- ══ TREK MODAL ══ -->
    <div v-if="showTrekModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4" @click.self="showTrekModal = false">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-lg modal-animate overflow-y-auto max-h-[90vh]">
        <div class="flex items-center justify-between px-6 py-4 border-b border-gray-100">
          <h3 class="font-bold text-gray-900">{{ isEditingTrek ? 'Update Trek Trail' : 'Create Trek Trail' }}</h3>
          <button @click="showTrekModal = false" class="w-8 h-8 flex items-center justify-center rounded-xl hover:bg-gray-100 text-gray-400 transition-all">✕</button>
        </div>
        <form @submit.prevent="saveTrek()" class="p-6 space-y-4">
          <div class="space-y-1.5">
            <label class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Trek Name</label>
            <input type="text" v-model="trekForm.trek_name" required class="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-green-500 bg-gray-50"/>
          </div>
          <div class="space-y-1.5">
            <label class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Location</label>
            <input type="text" v-model="trekForm.location" required class="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-green-500 bg-gray-50"/>
          </div>
          <div class="space-y-1.5">
            <label class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Description</label>
            <textarea v-model="trekForm.description" rows="2" class="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-green-500 bg-gray-50 resize-none"></textarea>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div class="space-y-1.5">
              <label class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Difficulty</label>
              <select v-model="trekForm.difficulty" required class="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-green-500 bg-gray-50">
                <option>Easy</option><option>Moderate</option><option>Hard</option>
              </select>
            </div>
            <div class="space-y-1.5">
              <label class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Duration (days)</label>
              <input type="number" v-model="trekForm.duration_days" required class="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-green-500 bg-gray-50"/>
            </div>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div class="space-y-1.5">
              <label class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Total Slots</label>
              <input type="number" v-model="trekForm.total_slots" required class="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-green-500 bg-gray-50"/>
            </div>
            <div class="space-y-1.5">
              <label class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Assign Guide</label>
              <select v-model="trekForm.assigned_staff_id" class="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-green-500 bg-gray-50">
                <option :value="null">-- Unassigned --</option>
                <option v-for="s in staffList" :key="s.id" :value="s.id">{{ s.name }}</option>
              </select>
            </div>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div class="space-y-1.5">
              <label class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Start Date</label>
              <input type="date" v-model="trekForm.start_date" required class="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-green-500 bg-gray-50"/>
            </div>
            <div class="space-y-1.5">
              <label class="text-xs font-semibold text-gray-500 uppercase tracking-wide">End Date</label>
              <input type="date" v-model="trekForm.end_date" required class="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-green-500 bg-gray-50"/>
            </div>
          </div>
          <div class="flex gap-3 pt-2">
            <button type="button" @click="showTrekModal = false" class="flex-1 border border-gray-200 text-gray-600 font-semibold py-2.5 rounded-xl hover:bg-gray-50 text-sm transition-all">Cancel</button>
            <button type="submit" class="flex-1 bg-green-700 hover:bg-green-800 text-white font-semibold py-2.5 rounded-xl text-sm transition-all shadow-sm">Save</button>
          </div>
        </form>
      </div>
    </div>

  </div>
</template>

<script>
import { ref, onMounted, reactive, computed } from 'vue';
import { useRouter } from 'vue-router';
import api from '../services/api';
import store from '../store';
import { Chart } from 'chart.js/auto';

const TREK_IMAGES = [
  'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=400&q=80',
  'https://images.unsplash.com/photo-1551632811-561732d1e306?w=400&q=80',
  'https://images.unsplash.com/photo-1486870591958-9b9d0d1dda99?w=400&q=80',
  'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&q=80',
  'https://images.unsplash.com/photo-1519681393784-d120267933ba?w=400&q=80',
  'https://images.unsplash.com/photo-1434394354979-a235cd36269d?w=400&q=80',
];
function getTrekImage(name) {
  if (!name) return TREK_IMAGES[0];
  let h = 0;
  for (let i = 0; i < name.length; i++) h = (h * 31 + name.charCodeAt(i)) & 0xffffffff;
  return TREK_IMAGES[Math.abs(h) % TREK_IMAGES.length];
}

export default {
  setup() {
    const router = useRouter();
    const user = computed(() => store.state.user);
    const handleLogout = () => { store.logout(); router.push({ name: 'Login' }); };

    const activeTab = ref('overview');
    const showStaffModal = ref(false);
    const showTrekModal = ref(false);

    const metrics = ref({ total_treks: 0, total_staff: 0, total_trekkers: 0, total_bookings: 0, active_treks: 0, completed_treks: 0 });
    const staffList = ref([]);
    const treks = ref([]);
    const usersList = ref([]);
    const userSearchQuery = ref('');
    const staffSearchQuery = ref('');
    const trekSearchQuery = ref('');
    const bookingSearchQuery = ref('');
    const bookingsList = ref([]);

    const isEditingStaff = ref(false);
    const staffForm = reactive({ id: null, name: '', email: '', password: '', phone: '', experience: 0, certifications: '', emergency_contact: '' });

    const isEditingTrek = ref(false);
    const trekForm = reactive({ id: null, trek_name: '', location: '', description: '', difficulty: 'Easy', duration_days: 1, total_slots: 10, assigned_staff_id: null, start_date: '', end_date: '' });

    let diffChart = null, bksChart = null, monthlyChart = null;

    const navItems = [
      { key: 'overview', label: 'Overview',   icon: '🏠' },
      { key: 'staff',    label: 'Staff',       icon: '🧑‍💼' },
      { key: 'treks',    label: 'Trek Trails', icon: '🏔' },
      { key: 'users',    label: 'Users',       icon: '👥' },
      { key: 'bookings', label: 'Bookings',    icon: '📋' },
      { key: 'reports',  label: 'Reports',     icon: '📊' },
    ];

    const quickNav = [
      { tab: 'staff',    label: 'Staff',       sub: 'Manage guides',    icon: '🧑‍💼', img: 'https://images.unsplash.com/photo-1551632811-561732d1e306?w=300&q=60' },
      { tab: 'treks',    label: 'Trek Trails', sub: 'Create & manage',  icon: '🏔', img: 'https://images.unsplash.com/photo-1486870591958-9b9d0d1dda99?w=300&q=60' },
      { tab: 'users',    label: 'Users',       sub: 'Trekker registry', icon: '👥', img: 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=300&q=60' },
      { tab: 'bookings', label: 'Bookings',    sub: 'All reservations', icon: '📋', img: 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=300&q=60' },
    ];

    const currentPageTitle = computed(() => navItems.find(i => i.key === activeTab.value)?.label || 'Admin');

    const formatLabel = (str) => str.replace(/_/g, ' ');

    const fetchStaff = async () => {
      try { const res = await api.get('/api/admin/staff', { params: { search: staffSearchQuery.value } }); staffList.value = res.data; }
      catch (err) { console.error(err); }
    };
    const fetchTreks = async () => {
      try { const res = await api.get('/api/treks', { params: { location: trekSearchQuery.value } }); treks.value = res.data; }
      catch (err) { console.error(err); }
    };
    const fetchBookings = async () => {
      try { const res = await api.get('/api/admin/bookings', { params: { search: bookingSearchQuery.value } }); bookingsList.value = res.data; }
      catch (err) { console.error(err); }
    };
    const fetchData = async () => {
      try {
        const statsRes = await api.get('/api/admin/dashboard');
        metrics.value = statsRes.data;
        await fetchStaff(); await fetchTreks(); await fetchBookings();
      } catch (err) { console.error(err); }
    };
    const fetchUsers = async () => {
      try { const res = await api.get('/api/admin/users', { params: { search: userSearchQuery.value } }); usersList.value = res.data; }
      catch (err) { console.error(err); }
    };

    const resetStaffForm = () => { isEditingStaff.value = false; Object.assign(staffForm, { id: null, name: '', email: '', password: '', phone: '', experience: 0, certifications: '', emergency_contact: '' }); };
    const editStaff = (s) => { isEditingStaff.value = true; Object.assign(staffForm, { id: s.id, name: s.name, email: s.email, password: '', phone: s.phone, experience: s.experience, certifications: s.certifications, emergency_contact: s.emergency_contact }); };

    const saveStaff = async () => {
      try {
        if (isEditingStaff.value) await api.put(`/api/admin/staff/${staffForm.id}`, staffForm);
        else await api.post('/api/admin/staff', staffForm);
        window.triggerToast(isEditingStaff.value ? 'Staff updated' : 'Staff added', 'success');
        showStaffModal.value = false;
        fetchData();
      } catch (err) { window.triggerToast(err.response?.data?.error || 'Failed', 'error'); }
    };
    const toggleStaffBlacklist = async (s) => { try { await api.put(`/api/admin/staff/${s.id}/status`, { is_blacklisted: !s.is_blacklisted }); window.triggerToast('Updated', 'success'); fetchData(); } catch (e) { window.triggerToast('Failed', 'error'); } };
    const toggleStaffActive = async (s) => { try { await api.put(`/api/admin/staff/${s.id}/status`, { is_active: !s.is_active }); window.triggerToast('Updated', 'success'); fetchData(); } catch (e) { window.triggerToast('Failed', 'error'); } };
    const deleteStaff = async (id) => { if (!confirm('Delete this staff member?')) return; try { await api.delete(`/api/admin/staff/${id}`); window.triggerToast('Deleted', 'success'); fetchData(); } catch (e) { window.triggerToast('Failed', 'error'); } };

    const toggleUserBlacklist = async (u) => { try { await api.put(`/api/admin/user/${u.id}/status`, { is_blacklisted: !u.is_blacklisted }); window.triggerToast('Updated', 'success'); fetchUsers(); } catch (e) { window.triggerToast('Failed', 'error'); } };
    const toggleUserActive = async (u) => { try { await api.put(`/api/admin/user/${u.id}/status`, { is_active: !u.is_active }); window.triggerToast('Updated', 'success'); fetchUsers(); } catch (e) { window.triggerToast('Failed', 'error'); } };

    const resetTrekForm = () => { isEditingTrek.value = false; Object.assign(trekForm, { id: null, trek_name: '', location: '', description: '', difficulty: 'Easy', duration_days: 1, total_slots: 10, assigned_staff_id: null, start_date: '', end_date: '' }); };
    const editTrek = (t) => { isEditingTrek.value = true; Object.assign(trekForm, { id: t.id, trek_name: t.trek_name, location: t.location, description: t.description, difficulty: t.difficulty, duration_days: t.duration_days, total_slots: t.total_slots, assigned_staff_id: t.assigned_staff_id, start_date: t.start_date, end_date: t.end_date }); };

    const saveTrek = async () => {
      try {
        if (isEditingTrek.value) await api.put(`/api/admin/trek/${trekForm.id}`, trekForm);
        else await api.post('/api/admin/trek', trekForm);
        window.triggerToast(isEditingTrek.value ? 'Trek updated' : 'Trek created', 'success');
        showTrekModal.value = false;
        fetchData();
      } catch (err) { window.triggerToast(err.response?.data?.error || 'Failed', 'error'); }
    };
    const updateTrekStatus = async (id, status) => { try { await api.put(`/api/admin/trek/${id}`, { status }); window.triggerToast(`Trek marked ${status}`, 'success'); fetchData(); } catch (e) { window.triggerToast('Failed', 'error'); } };
    const deleteTrek = async (id) => { if (!confirm('Delete this trek?')) return; try { await api.delete(`/api/admin/trek/${id}`); window.triggerToast('Deleted', 'success'); fetchData(); } catch (e) { window.triggerToast('Failed', 'error'); } };

    const openReportsTab = () => { activeTab.value = 'reports'; setTimeout(renderCharts, 200); };
    const renderCharts = async () => {
      try {
        const res = await api.get('/api/admin/reports/statistics');
        const data = res.data;
        if (diffChart) diffChart.destroy();
        if (bksChart) bksChart.destroy();
        if (monthlyChart) monthlyChart.destroy();
        const opts = { responsive: true, maintainAspectRatio: false, plugins: { legend: { labels: { color: '#374151', font: { size: 11 } } } } };
        diffChart = new Chart(document.getElementById('difficultyChart'), { type: 'doughnut', data: { labels: Object.keys(data.difficulty), datasets: [{ data: Object.values(data.difficulty), backgroundColor: ['#10b981','#f59e0b','#ef4444'], borderWidth: 0 }] }, options: opts });
        bksChart  = new Chart(document.getElementById('bookingsChart'),   { type: 'pie',       data: { labels: Object.keys(data.bookings),   datasets: [{ data: Object.values(data.bookings),   backgroundColor: ['#6366f1','#f43f5e','#06b6d4'], borderWidth: 0 }] }, options: opts });
        const ml = Object.keys(data.monthly_bookings).sort();
        monthlyChart = new Chart(document.getElementById('monthlyBookingsChart'), { type: 'bar', data: { labels: ml, datasets: [{ label: 'Bookings', data: ml.map(k => data.monthly_bookings[k]), backgroundColor: '#16a34a', borderRadius: 6 }] }, options: { ...opts, scales: { x: { grid: { display: false }, ticks: { color: '#6b7280', font: { size: 10 } } }, y: { grid: { color: '#f3f4f6' }, ticks: { color: '#6b7280', font: { size: 10 }, stepSize: 1 }, beginAtZero: true } } } });
      } catch (e) { console.error(e); }
    };

    const triggerMonthlyReport = async () => {
      try {
        const res = await api.post('/api/admin/reports/trigger');
        const dlRes = await api.get(`/api/admin/reports/download/${res.data.filename}`, { responseType: 'blob' });
        const url = URL.createObjectURL(new Blob([dlRes.data], { type: 'text/html' }));
        const a = document.createElement('a'); a.href = url; a.download = res.data.filename;
        document.body.appendChild(a); a.click(); a.remove(); URL.revokeObjectURL(url);
        window.triggerToast('Report downloaded!', 'success');
      } catch (err) { window.triggerToast(err.response?.data?.error || 'Failed', 'error'); }
    };

    const formatDate = (str) => str ? str.split('T')[0] : '';

    onMounted(() => { fetchData(); fetchUsers(); });

    return {
      user, handleLogout, activeTab, showStaffModal, showTrekModal,
      metrics, staffList, treks, usersList, bookingsList,
      userSearchQuery, staffSearchQuery, trekSearchQuery, bookingSearchQuery,
      staffForm, isEditingStaff, trekForm, isEditingTrek,
      navItems, quickNav, currentPageTitle,
      getTrekImage, formatLabel, formatDate,
      fetchStaff, fetchTreks, fetchBookings, fetchUsers,
      resetStaffForm, editStaff, saveStaff, toggleStaffBlacklist, toggleStaffActive, deleteStaff,
      toggleUserBlacklist, toggleUserActive,
      resetTrekForm, editTrek, saveTrek, updateTrekStatus, deleteTrek,
      openReportsTab, triggerMonthlyReport,
    };
  }
};
</script>

<style scoped>
.modal-animate { animation: modalIn 0.2s cubic-bezier(0.34,1.56,0.64,1) both; }
@keyframes modalIn { from { opacity:0; transform:scale(0.95) translateY(8px); } to { opacity:1; transform:scale(1) translateY(0); } }
</style>
