import { create } from 'zustand';

interface UserInfo {
  name: string;
  title: string;
  company: string;
  email: string;
  phone: string;
  website: string;
  linkedin: string;
  twitter: string;
  github: string;
}

interface CardStyle {
  template: string;
  primaryColor: string;
  secondaryColor: string;
  font: string;
  layout: string;
}

interface CardState {
  userInfo: UserInfo;
  cardStyle: CardStyle;
  exportFormat: string;
  setUserInfo: (info: Partial<UserInfo>) => void;
  setCardStyle: (style: Partial<CardStyle>) => void;
  setExportFormat: (format: string) => void;
}

const useCardStore = create<CardState>((set) => ({
  userInfo: {
    name: '张三',
    title: '前端开发工程师',
    company: '科技公司',
    email: 'zhangsan@example.com',
    phone: '13800138000',
    website: 'https://example.com',
    linkedin: 'linkedin.com/in/zhangsan',
    twitter: '@zhangsan',
    github: 'github.com/zhangsan',
  },
  cardStyle: {
    template: 'template1',
    primaryColor: '#3b82f6',
    secondaryColor: '#6366f1',
    font: 'Inter',
    layout: 'standard',
  },
  exportFormat: 'png',
  setUserInfo: (info) => set((state) => ({
    userInfo: { ...state.userInfo, ...info },
  })),
  setCardStyle: (style) => set((state) => ({
    cardStyle: { ...state.cardStyle, ...style },
  })),
  setExportFormat: (format) => set({ exportFormat: format }),
}));

export default useCardStore;