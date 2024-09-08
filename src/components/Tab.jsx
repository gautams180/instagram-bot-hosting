import React from 'react'

const Tab = ({ tabData, operationType, setOperationType }) => {
  return (
    <div
        className='flex bg-richblack-800 p-1 gap-x-1 mb-6 rounded-full max-w-max'
    >
        {
            tabData.map( (tab) => (
                <button
                    key={tab.id}
                    onClick={() => setOperationType(tab.type)}
                    className={`${
                        operationType === tab.type
                        ? "bg-richblack-900 text-richblack-5"
                        : "bg-transparent text-richblack-200"
                    } p-2 rounded-full transition-all duration-200`}
                >
                    {tab.tabName}
                </button>
            ))
        }
    </div>
  )
}

export default Tab