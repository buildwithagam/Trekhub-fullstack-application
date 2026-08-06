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
        <span class="ml-auto text-xs font-bold bg-orange-500/20 text-orange-400 border border-orange-500/30 px-2 py-0.5 rounded-full">Staff</span>
      </div>

      <!-- Nav -->
      <nav class="flex-1 py-4 px-3 space-y-0.5">
        <button
          class="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all text-left bg-green-700 text-white">
          <span class="text-base">🏔</span> My Treks
        </button>
        <button
          class="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all text-left text-slate-400 hover:bg-slate-800 hover:text-white">
          <span class="text-base">👥</span> Participants
        </button>
        <button
          class="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all text-left text-slate-400 hover:bg-slate-800 hover:text-white">
          <span class="text-base">📋</span> Schedule
        </button>
      </nav>

      <!-- Mountain image card -->
      <div class="mx-3 mb-3 rounded-2xl overflow-hidden relative h-36">
        <img src="https://images.unsplash.com/photo-1551632811-561732d1e306?w=400&q=70"
          class="w-full h-full object-cover"/>
        <div class="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent flex items-end p-3">
          <p class="text-white text-xs font-semibold">Guide every expedition</p>
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
        <span class="text-gray-700 font-semibold text-sm">Staff Portal</span>
        <div class="flex items-center gap-3 ml-auto">
          <!-- Role Switcher -->
          <div class="relative" ref="roleSwitcherRef">
            <button @click="showRoleSwitcher = !showRoleSwitcher" :disabled="switchingRole"
              class="flex items-center gap-2 border border-green-200 bg-green-50 hover:bg-green-100 text-green-700 font-semibold px-3 py-2 rounded-xl text-xs transition-all disabled:opacity-60">
              <svg v-if="switchingRole" class="w-3.5 h-3.5 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
              <span v-else>🔄</span>
              {{ switchingRole ? 'Switching…' : 'Switch Role' }}
              <svg class="w-3.5 h-3.5 transition-transform" :class="showRoleSwitcher ? 'rotate-180':''" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
              </svg>
            </button>
            <div v-if="showRoleSwitcher" class="absolute right-0 top-full mt-2 w-64 bg-white border border-gray-200 rounded-2xl shadow-xl z-50 overflow-hidden">
              <div class="px-4 py-2.5 bg-gray-50 border-b border-gray-100">
                <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide">Demo — Switch Dashboard</p>
              </div>
              <div class="divide-y divide-gray-50">
                <button v-for="r in demoRoles" :key="r.role" @click="switchRole(r)"
                  class="w-full flex items-center gap-3 px-4 py-3 hover:bg-green-50 transition-colors text-left"
                  :class="r.current ? 'bg-green-50' : ''">
                  <span class="w-9 h-9 rounded-xl flex items-center justify-center text-lg shrink-0" :class="r.bg">{{ r.icon }}</span>
                  <div class="flex-1">
                    <p class="text-sm font-semibold text-gray-900">{{ r.label }}</p>
                    <p class="text-xs text-gray-400">{{ r.email }}</p>
                  </div>
                  <span v-if="r.current" class="text-xs font-bold text-green-600 bg-green-100 px-2 py-0.5 rounded-full">Active</span>
                </button>
              </div>
            </div>
          </div>

          <div class="flex items-center gap-2.5 pl-3 border-l border-gray-200">
            <div class="w-8 h-8 rounded-full bg-orange-600 flex items-center justify-center text-white font-bold text-sm shadow">
              {{ (user?.name || 'S').charAt(0).toUpperCase() }}
            </div>
            <div class="hidden sm:block leading-tight">
              <p class="text-sm font-semibold text-gray-900">{{ user?.name }}</p>
              <p class="text-xs text-orange-500 font-semibold">Trek Guide</p>
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

        <!-- Hero banner -->
        <div class="relative rounded-2xl overflow-hidden h-36 mb-6">
          <img src="https://images.unsplash.com/photo-1486870591958-9b9d0d1dda99?w=1200&q=70"
            class="w-full h-full object-cover"/>
          <div class="absolute inset-0 bg-gradient-to-r from-slate-900/80 to-transparent flex items-center px-8">
            <div>
              <h1 class="text-white text-2xl font-black" style="font-family:'Poppins',sans-serif">
                Welcome, {{ user?.name?.split(' ')[0] }}! 🧗
              </h1>
              <p class="text-slate-300 text-sm mt-1">{{ assignedTreks.length }} trek{{ assignedTreks.length !== 1 ? 's' : '' }} assigned to you</p>
            </div>
          </div>
        </div>

        <!-- Stats row -->
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <div class="bg-white rounded-2xl border border-gray-100 p-5 shadow-sm">
            <p class="text-xs text-gray-400 font-semibold uppercase tracking-wide">Total Assigned</p>
            <p class="text-3xl font-black text-gray-900 mt-1" style="font-family:'Poppins',sans-serif">{{ assignedTreks.length }}</p>
            <p class="text-xs text-green-600 mt-1 font-medium">All treks</p>
          </div>
          <div class="bg-white rounded-2xl border border-gray-100 p-5 shadow-sm">
            <p class="text-xs text-gray-400 font-semibold uppercase tracking-wide">Active Now</p>
            <p class="text-3xl font-black text-gray-900 mt-1" style="font-family:'Poppins',sans-serif">{{ assignedTreks.filter(t=>t.status==='Open').length }}</p>
            <p class="text-xs text-blue-500 mt-1 font-medium">Open treks</p>
          </div>
          <div class="bg-white rounded-2xl border border-gray-100 p-5 shadow-sm">
            <p class="text-xs text-gray-400 font-semibold uppercase tracking-wide">Total Participants</p>
            <p class="text-3xl font-black text-gray-900 mt-1" style="font-family:'Poppins',sans-serif">{{ assignedTreks.reduce((s,t)=>s+(t.participant_count||0),0) }}</p>
            <p class="text-xs text-orange-500 mt-1 font-medium">Across all treks</p>
          </div>
          <div class="bg-white rounded-2xl border border-gray-100 p-5 shadow-sm">
            <p class="text-xs text-gray-400 font-semibold uppercase tracking-wide">Completed</p>
            <p class="text-3xl font-black text-gray-900 mt-1" style="font-family:'Poppins',sans-serif">{{ assignedTreks.filter(t=>t.status==='Completed').length }}</p>
            <p class="text-xs text-purple-500 mt-1 font-medium">Finished treks</p>
          </div>
        </div>

        <!-- Trek cards -->
        <h2 class="font-bold text-gray-900 text-lg mb-4" style="font-family:'Poppins',sans-serif">My Assigned Treks</h2>
        <div class="grid sm:grid-cols-2 xl:grid-cols-3 gap-5">
          <div v-for="t in assignedTreks" :key="t.id"
            class="bg-white rounded-2xl border border-gray-100 shadow-sm hover:shadow-lg hover:-translate-y-1 transition-all duration-200 overflow-hidden group">
            <!-- Trek image -->
            <div class="relative h-44 overflow-hidden">
              <img :src="getTrekImage(t.trek_name)" :alt="t.trek_name"
                class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"/>
              <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
              <span class="absolute top-3 right-3 text-xs font-bold px-2.5 py-1 rounded-full"
                :class="t.status==='Open' ? 'bg-green-500 text-white' : t.status==='Pending' ? 'bg-yellow-500 text-white' : t.status==='Completed' ? 'bg-blue-500 text-white' : 'bg-gray-600 text-white'">
                {{ t.status }}
              </span>
              <div class="absolute bottom-3 left-3 right-3">
                <h3 class="text-white font-bold text-base leading-tight truncate">{{ t.trek_name }}</h3>
                <p class="text-slate-300 text-xs mt-0.5">📍 {{ t.location }}</p>
              </div>
            </div>

            <!-- Body -->
            <div class="p-4 space-y-3">
              <div class="grid grid-cols-2 gap-2 text-xs">
                <div class="bg-gray-50 rounded-xl p-2.5">
                  <p class="text-gray-400 font-medium">Duration</p>
                  <p class="text-gray-800 font-bold mt-0.5">{{ t.duration_days }} days</p>
                </div>
                <div class="bg-gray-50 rounded-xl p-2.5">
                  <p class="text-gray-400 font-medium">Participants</p>
                  <p class="text-gray-800 font-bold mt-0.5">{{ t.participant_count || 0 }}</p>
                </div>
              </div>

              <!-- Date range -->
              <div class="flex items-center gap-2 text-xs text-gray-500 bg-orange-50 border border-orange-100 rounded-xl px-3 py-2">
                <svg class="w-3.5 h-3.5 text-orange-400 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <rect x="3" y="4" width="18" height="18" rx="2" stroke-width="2"/><line x1="16" y1="2" x2="16" y2="6" stroke-width="2" stroke-linecap="round"/><line x1="8" y1="2" x2="8" y2="6" stroke-width="2" stroke-linecap="round"/><line x1="3" y1="10" x2="21" y2="10" stroke-width="2"/>
                </svg>
                <span class="font-medium text-orange-700">{{ t.start_date }} → {{ t.end_date }}</span>
              </div>

              <!-- Slot progress -->
              <div>
                <div class="flex justify-between text-xs text-gray-400 mb-1.5">
                  <span>Booking Capacity</span>
                  <span class="font-semibold text-gray-700">{{ t.total_slots - t.available_slots }} / {{ t.total_slots }}</span>
                </div>
                <div class="h-2 bg-gray-100 rounded-full overflow-hidden">
                  <div class="h-full bg-green-500 rounded-full transition-all"
                    :style="{width: t.total_slots ? ((t.total_slots - t.available_slots) / t.total_slots * 100) + '%' : '0%'}"></div>
                </div>
              </div>

              <!-- Actions -->
              <div class="flex items-center gap-2 flex-wrap pt-1">
                <button @click="openParticipantsModal(t); showParticipantsModal = true"
                  class="flex items-center gap-1.5 text-xs font-semibold text-blue-600 border border-blue-200 hover:bg-blue-50 px-3 py-1.5 rounded-xl transition-all">
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                  Participants ({{ t.participant_count || 0 }})
                </button>
                <button @click="openSlotsModal(t); showSlotsModal = true"
                  class="flex items-center gap-1.5 text-xs font-semibold text-orange-600 border border-orange-200 hover:bg-orange-50 px-3 py-1.5 rounded-xl transition-all">
                  ✏ Edit Slots
                </button>
              </div>
              <div class="flex items-center gap-2 flex-wrap">
                <button @click="changeStatus(t.id,'Open')" v-if="t.status==='Approved'||t.status==='Closed'"
                  class="text-xs font-semibold text-green-700 bg-green-100 hover:bg-green-200 px-3 py-1.5 rounded-xl transition-all">
                  ▶ Start / Open
                </button>
                <button @click="changeStatus(t.id,'Completed')" v-if="t.status==='Open'"
                  class="text-xs font-semibold text-blue-700 bg-blue-100 hover:bg-blue-200 px-3 py-1.5 rounded-xl transition-all">
                  ✓ Mark Complete
                </button>
              </div>
            </div>
          </div>

          <div v-if="assignedTreks.length === 0"
            class="col-span-full flex flex-col items-center justify-center py-20 text-gray-400">
            <span class="text-5xl mb-3">🏔</span>
            <p class="font-semibold text-gray-600">No treks assigned yet</p>
            <p class="text-sm mt-1">You'll see your expeditions here once assigned by admin</p>
          </div>
        </div>

      </main>
    </div>

    <!-- ══ PARTICIPANTS MODAL ══ -->
    <div v-if="showParticipantsModal"
      class="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4"
      @click.self="showParticipantsModal = false">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-2xl modal-animate overflow-hidden">
        <div class="flex items-center justify-between px-6 py-4 border-b border-gray-100">
          <div>
            <h3 class="font-bold text-gray-900">Participants</h3>
            <p class="text-xs text-gray-400 mt-0.5">{{ selectedTrek?.trek_name }}</p>
          </div>
          <button @click="showParticipantsModal = false" class="w-8 h-8 flex items-center justify-center rounded-xl hover:bg-gray-100 text-gray-400 transition-all">✕</button>
        </div>
        <div class="overflow-y-auto max-h-[60vh]">
          <table class="w-full text-sm">
            <thead>
              <tr class="bg-gray-50 border-b border-gray-100">
                <th class="text-left px-5 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide">Trekker</th>
                <th class="text-left px-5 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide hidden md:table-cell">Phone</th>
                <th class="text-left px-5 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide">Status</th>
                <th class="text-left px-5 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide hidden md:table-cell">Remarks</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-50">
              <tr v-for="p in participants" :key="p.booking_id" class="hover:bg-gray-50">
                <td class="px-5 py-3.5">
                  <p class="font-semibold text-gray-900">{{ p.name }}</p>
                  <p class="text-xs text-gray-400">{{ p.email }}</p>
                </td>
                <td class="px-5 py-3.5 text-gray-500 hidden md:table-cell text-xs">{{ p.phone || '—' }}</td>
                <td class="px-5 py-3.5">
                  <span class="inline-flex px-2.5 py-1 rounded-full text-xs font-semibold bg-green-100 text-green-700">{{ p.booking_status }}</span>
                </td>
                <td class="px-5 py-3.5 text-gray-400 text-xs hidden md:table-cell">{{ p.remarks || '—' }}</td>
              </tr>
              <tr v-if="participants.length === 0">
                <td colspan="4" class="text-center py-12 text-gray-400">
                  <span class="text-3xl block mb-2">👥</span>No participants yet.
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- ══ SLOTS MODAL ══ -->
    <div v-if="showSlotsModal"
      class="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4"
      @click.self="showSlotsModal = false">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-sm modal-animate">
        <div class="flex items-center justify-between px-6 py-4 border-b border-gray-100">
          <h3 class="font-bold text-gray-900">Edit Slots</h3>
          <button @click="showSlotsModal = false" class="w-8 h-8 flex items-center justify-center rounded-xl hover:bg-gray-100 text-gray-400 transition-all">✕</button>
        </div>
        <form @submit.prevent="updateSlots()" class="p-6 space-y-4">
          <p class="text-sm text-gray-600">Update available slots for <span class="font-semibold text-gray-900">{{ selectedTrek?.trek_name }}</span></p>
          <div class="space-y-1.5">
            <label class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Available Slots</label>
            <input type="number" v-model="slotsForm.available_slots" required min="0"
              class="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-green-500 bg-gray-50"/>
          </div>
          <div class="flex gap-3">
            <button type="button" @click="showSlotsModal = false" class="flex-1 border border-gray-200 text-gray-600 font-semibold py-2.5 rounded-xl hover:bg-gray-50 text-sm transition-all">Cancel</button>
            <button type="submit" class="flex-1 bg-green-700 hover:bg-green-800 text-white font-semibold py-2.5 rounded-xl text-sm transition-all shadow-sm">Update</button>
          </div>
        </form>
      </div>
    </div>

  </div>
</template>

<script>
import { ref, onMounted, onBeforeUnmount, reactive, computed } from 'vue';
import { useRouter } from 'vue-router';
import api from '../services/api';
import store from '../store';
import { DEMO_ROLES, switchToRole } from '../services/roleSwitcher';

const DUMMY_ASSIGNED_TREKS = [
  { id:1, trek_name:'Kashmir Great Lakes',   location:'Srinagar, Kashmir',           description:'A stunning trek through the most beautiful alpine lakes in India.',    difficulty:'Moderate', duration_days:7, total_slots:15, available_slots:8,  start_date:'2026-08-10', end_date:'2026-08-17', status:'Open',      participant_count:7  },
  { id:2, trek_name:'Valley of Flowers',     location:'Chamoli, Uttarakhand',        description:'UNESCO World Heritage site filled with rare alpine blooms.',            difficulty:'Easy',     duration_days:6, total_slots:20, available_slots:14, start_date:'2026-08-01', end_date:'2026-08-07', status:'Open',      participant_count:6  },
  { id:3, trek_name:'Roopkund Mystery Lake', location:'Garhwal, Uttarakhand',        description:'High altitude glacial lake trek with mysterious skeletal remains.',      difficulty:'Hard',     duration_days:8, total_slots:10, available_slots:6,  start_date:'2026-09-15', end_date:'2026-09-23', status:'Pending',   participant_count:0  },
  { id:4, trek_name:'Hampta Pass Trek',      location:'Manali, Himachal Pradesh',    description:'A thrilling crossover trek connecting Kullu and Spiti valley.',         difficulty:'Moderate', duration_days:5, total_slots:15, available_slots:8,  start_date:'2026-08-20', end_date:'2026-08-25', status:'Approved',  participant_count:7  },
];

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

    const showRoleSwitcher = ref(false);
    const switchingRole = ref(false);
    const roleSwitcherRef = ref(null);
    const demoRoles = computed(() =>
      DEMO_ROLES.map(r => ({ ...r, current: user.value?.role === r.role }))
    );
    const switchRole = async (r) => {
      if (r.current || switchingRole.value) return;
      switchingRole.value = true;
      showRoleSwitcher.value = false;
      const ok = await switchToRole(r.role, router);
      if (!ok) window.triggerToast('Failed to switch — try again in 30s', 'error');
      switchingRole.value = false;
    };
    const handleOutside = (e) => { if (roleSwitcherRef.value && !roleSwitcherRef.value.contains(e.target)) showRoleSwitcher.value = false; };

    const assignedTreks = ref([]);
    const selectedTrek = ref(null);
    const participants = ref([]);
    const showParticipantsModal = ref(false);
    const showSlotsModal = ref(false);

    const slotsForm = reactive({ available_slots: 0 });

    const fetchAssignedTreks = async () => {
      try {
        const res = await api.get('/api/staff/treks');
        assignedTreks.value = res.data?.length ? res.data : DUMMY_ASSIGNED_TREKS;
      } catch (err) {
        if (!assignedTreks.value.length) assignedTreks.value = DUMMY_ASSIGNED_TREKS;
      }
    };

    const openParticipantsModal = async (trek) => {
      selectedTrek.value = trek;
      participants.value = [];
      try { const res = await api.get(`/api/staff/trek/${trek.id}/participants`); participants.value = res.data; }
      catch (err) { window.triggerToast('Failed to fetch participants', 'error'); }
    };

    const openSlotsModal = (trek) => {
      selectedTrek.value = trek;
      slotsForm.available_slots = trek.available_slots;
    };

    const updateSlots = async () => {
      try {
        await api.put(`/api/staff/trek/${selectedTrek.value.id}`, { available_slots: slotsForm.available_slots });
        window.triggerToast('Slots updated!', 'success');
        showSlotsModal.value = false;
        fetchAssignedTreks();
      } catch (err) { window.triggerToast(err.response?.data?.error || 'Failed', 'error'); }
    };

    const changeStatus = async (trekId, status) => {
      try { await api.put(`/api/staff/trek/${trekId}`, { status }); window.triggerToast(`Status → ${status}`, 'success'); fetchAssignedTreks(); }
      catch (err) { window.triggerToast(err.response?.data?.error || 'Failed', 'error'); }
    };

    let pollInterval = null;
    onMounted(() => {
      // Pre-fill dummy data instantly
      assignedTreks.value = DUMMY_ASSIGNED_TREKS;
      document.addEventListener('click', handleOutside);
      // Fetch real data in background
      fetchAssignedTreks();
      pollInterval = setInterval(fetchAssignedTreks, 20000);
    });
    onBeforeUnmount(() => { if (pollInterval) clearInterval(pollInterval); document.removeEventListener('click', handleOutside); });

    return {
      user, handleLogout, showRoleSwitcher, switchingRole, roleSwitcherRef, demoRoles, switchRole,
      assignedTreks, selectedTrek, participants,
      showParticipantsModal, showSlotsModal,
      slotsForm, getTrekImage,
      openParticipantsModal, openSlotsModal, updateSlots, changeStatus,
    };
  }
};
</script>

<style scoped>
.modal-animate { animation: modalIn 0.2s cubic-bezier(0.34,1.56,0.64,1) both; }
@keyframes modalIn { from { opacity:0; transform:scale(0.95) translateY(8px); } to { opacity:1; transform:scale(1) translateY(0); } }
</style>
