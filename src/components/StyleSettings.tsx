import React from 'react';
import useCardStore from '../store';

const StyleSettings: React.FC = () => {
  const { cardStyle, setCardStyle } = useCardStore();

  const fonts = [
    { value: 'Inter', label: 'Inter' },
    { value: 'Arial', label: 'Arial' },
    { value: 'Helvetica', label: 'Helvetica' },
    { value: 'Georgia', label: 'Georgia' },
    { value: 'Times New Roman', label: 'Times New Roman' },
  ];

  const handleColorChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setCardStyle({ [name]: value });
  };

  const handleFontChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setCardStyle({ font: e.target.value });
  };

  return (
    <div className="p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">样式设置</h2>
      <div className="space-y-6">
        <div>
          <h3 className="text-lg font-semibold mb-4 text-gray-700">颜色设置</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">主色调</label>
              <div className="flex items-center gap-3">
                <input
                  type="color"
                  name="primaryColor"
                  value={cardStyle.primaryColor}
                  onChange={handleColorChange}
                  className="w-12 h-12 cursor-pointer border border-gray-300 rounded-md"
                />
                <input
                  type="text"
                  name="primaryColor"
                  value={cardStyle.primaryColor}
                  onChange={handleColorChange}
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="#3b82f6"
                />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">辅助色</label>
              <div className="flex items-center gap-3">
                <input
                  type="color"
                  name="secondaryColor"
                  value={cardStyle.secondaryColor}
                  onChange={handleColorChange}
                  className="w-12 h-12 cursor-pointer border border-gray-300 rounded-md"
                />
                <input
                  type="text"
                  name="secondaryColor"
                  value={cardStyle.secondaryColor}
                  onChange={handleColorChange}
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="#6366f1"
                />
              </div>
            </div>
          </div>
        </div>
        <div>
          <h3 className="text-lg font-semibold mb-4 text-gray-700">字体设置</h3>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">选择字体</label>
            <select
              value={cardStyle.font}
              onChange={handleFontChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              {fonts.map((font) => (
                <option key={font.value} value={font.value} style={{ fontFamily: font.value }}>
                  {font.label}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StyleSettings;