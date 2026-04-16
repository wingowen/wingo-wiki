import React, { useRef } from 'react';
import useCardStore from '../store';

const CardPreview: React.FC = () => {
  const { userInfo, cardStyle } = useCardStore();
  const cardRef = useRef<HTMLDivElement>(null);

  const getTemplateStyles = () => {
    switch (cardStyle.template) {
      case 'template1':
        return {
          background: `linear-gradient(135deg, ${cardStyle.primaryColor}, ${cardStyle.secondaryColor})`,
          color: 'white',
        };
      case 'template2':
        return {
          background: 'white',
          color: cardStyle.primaryColor,
          border: `2px solid ${cardStyle.primaryColor}`,
        };
      case 'template3':
        return {
          background: cardStyle.primaryColor,
          color: 'white',
          borderRadius: '12px',
        };
      default:
        return {
          background: `linear-gradient(135deg, ${cardStyle.primaryColor}, ${cardStyle.secondaryColor})`,
          color: 'white',
        };
    }
  };

  const templateStyles = getTemplateStyles();

  return (
    <div className="flex flex-col items-center justify-center p-6">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">卡片预览</h2>
      <div 
        ref={cardRef}
        data-card-preview
        className="relative w-96 h-64 shadow-xl transform transition-all duration-300 hover:scale-105 hover:rotate-1"
        style={{
          ...templateStyles,
          fontFamily: cardStyle.font,
        }}
      >
        <div className="absolute inset-0 p-6 flex flex-col justify-between">
          <div>
            <h3 className="text-2xl font-bold mb-1">{userInfo.name}</h3>
            <p className="text-sm opacity-90 mb-2">{userInfo.title}</p>
            <p className="text-sm opacity-80">{userInfo.company}</p>
          </div>
          <div className="space-y-2">
            <p className="text-sm flex items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                <polyline points="22,6 12,13 2,6"></polyline>
              </svg>
              {userInfo.email}
            </p>
            <p className="text-sm flex items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
              </svg>
              {userInfo.phone}
            </p>
            {userInfo.website && (
              <p className="text-sm flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <circle cx="12" cy="12" r="10"></circle>
                  <line x1="2" y1="12" x2="22" y2="12"></line>
                  <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
                </svg>
                {userInfo.website}
              </p>
            )}
          </div>
        </div>
      </div>
      <div className="mt-6 text-sm text-gray-500">
        提示：鼠标悬停卡片可查看3D效果
      </div>
    </div>
  );
};

export default CardPreview;