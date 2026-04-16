import React from 'react';
import useCardStore from '../store';

const TemplateSelector: React.FC = () => {
  const { cardStyle, setCardStyle } = useCardStore();

  const templates = [
    {
      id: 'template1',
      name: '渐变模板',
      style: {
        background: 'linear-gradient(135deg, #3b82f6, #6366f1)',
        color: 'white',
      },
    },
    {
      id: 'template2',
      name: '简约模板',
      style: {
        background: 'white',
        color: '#3b82f6',
        border: '2px solid #3b82f6',
      },
    },
    {
      id: 'template3',
      name: '纯色模板',
      style: {
        background: '#3b82f6',
        color: 'white',
        borderRadius: '12px',
      },
    },
  ];

  const handleTemplateSelect = (templateId: string) => {
    setCardStyle({ template: templateId });
  };

  return (
    <div className="p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">模板选择</h2>
      <div className="flex overflow-x-auto gap-4 pb-4">
        {templates.map((template) => (
          <div
            key={template.id}
            className={`flex-shrink-0 w-48 h-32 cursor-pointer rounded-md overflow-hidden transition-all duration-300 transform hover:scale-105 ${cardStyle.template === template.id ? 'ring-4 ring-blue-500' : 'shadow-md'}`}
            style={template.style}
            onClick={() => handleTemplateSelect(template.id)}
          >
            <div className="p-4 h-full flex flex-col justify-center items-center text-center">
              <h3 className="font-bold mb-2">{template.name}</h3>
              <p className="text-xs opacity-80">点击选择</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TemplateSelector;