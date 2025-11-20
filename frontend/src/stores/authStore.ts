import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { User, AuthResponse, RegisterData, LoginData } from '@/types';
import { authAPI } from '@/services/api';

interface AuthStore {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;

  login: (data: LoginData) => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
  setAuth: (response: AuthResponse) => void;
}

export const useAuthStore = create<AuthStore>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,

      setAuth: (response: AuthResponse) => {
        localStorage.setItem('token', response.access_token);
        set({
          user: response.user,
          token: response.access_token,
          isAuthenticated: true,
        });
      },

      login: async (data: LoginData) => {
        set({ isLoading: true });
        try {
          const response = await authAPI.login(data);
          get().setAuth(response);
        } finally {
          set({ isLoading: false });
        }
      },

      register: async (data: RegisterData) => {
        set({ isLoading: true });
        try {
          const response = await authAPI.register(data);
          get().setAuth(response);
        } finally {
          set({ isLoading: false });
        }
      },

      logout: () => {
        localStorage.removeItem('token');
        set({
          user: null,
          token: null,
          isAuthenticated: false,
        });
      },

      refreshUser: async () => {
        try {
          const user = await authAPI.getCurrentUser();
          set({ user });
        } catch (error) {
          // If refresh fails, logout
          get().logout();
        }
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);
