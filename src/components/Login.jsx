import React, { useEffect, useState } from 'react'
import Tab from './Tab';
import { FaEye } from "react-icons/fa";
import { FaEyeSlash } from "react-icons/fa";
import Papa from 'papaparse';
const BASE_URL = process.env.REACT_APP_BASE_URL
// const BASE_URL = import.meta.env.MODE === "development" ? "http://127.0.0.1:5000" : "/";

const Login = () => {


    const [operationType, setOperationType] = useState("Get");

    const [formData,setFormData] = useState({
        username: "",
        password: "",
    })

    const [showPassword, setShowPassword] = useState(false);

    const {username, password} = formData;
    
    const helloList = [];

    const tabData = [
        {
            id: 1,
            tabName: "Get Followers",
            type: "Get"
        },
        // {
        //     id: 2,
        //     tabName: "Follow People",
        //     type: "Follow"
        // }
    ]

    const handleOnChange = (e) => {
        setFormData((prevData) => ({
            ...prevData,
            [e.target.name]: e.target.value,
        }))
    }

    const handleFileUpload = (e) => {
        console.log(e);
        const file = e.target.files[0];
        console.log(file);
        Papa.parse(file, {
            header: true,
            complete: (results) => {
                console.log("results", results);
                const data = results.data;
                // console.log(data);
                
                data.forEach(item => {
                    const individualAccount = item.Accounts;
                    helloList.push(individualAccount);
                    // console.log(individualAccount);
                });
            }
        })
        console.log("List is here ",helloList);
        console.log("Form Data : ",formData);
        console.log("BASE_URL: ",BASE_URL)
    }

    const handleOnSubmit = async (e) => {
        try{

            if(operationType === "Get") {
                e.preventDefault();
                const response =  await fetch(`${BASE_URL}/api`,{
                    method:"POST",
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        username: formData.username,
                        password: formData.password,
                        list: helloList
                    })
                })
                
                if (!response.ok) {
                    throw new Error(`Response status: ${response.status}`);
                }
                console.log("Response in frontend ",response);
            }
        }
        catch(error) {
            console.log(error)
            console.log(error.message)
        }    
    }

  return (
    <div className='flex gap-5 transition-all duration-1000'>
        <div className='min-w-[400px] min-h-[400px] h-fit flex flex-col items-center p-5 bg-richblack-700 rounded-md sticky'>
            {/* Tab: Get followers OR Follow followers */}
            <Tab tabData={tabData} operationType={operationType} setOperationType={setOperationType} />

            {/* Form */}
            <form onSubmit={(e)=>handleOnSubmit(e)} className='w-full flex flex-col gap-y-4 transition-all duration-600' >
                        <label className='flex flex-col gap-y-1 items-start'>
                            <p className='text-white font-semibold text-md'>
                                Username, email or phone number
                            </p>
                            <input 
                                required
                                type='text'
                                name='username'
                                value={username}
                                onChange={handleOnChange}
                                placeholder='Enter Username'
                                style={{
                                    boxShadow: "inset 0px -1px 0px rgba(255, 255, 255, 0.18)",
                                }}
                                className='w-full rounded-[0.5rem] bg-richblack-800 p-[12px] text-richblack-5'
                            />
                        </label>
                        <label className='relative flex flex-col gap-y-1 items-start'>
                            <p className='text-white font-semibold text-md'>
                                Password
                            </p>
                            <input 
                                required
                                type={showPassword ? "text" : "password"}
                                name='password'
                                value={password}
                                onChange={handleOnChange}
                                placeholder='Enter Password'
                                style={{
                                    boxShadow: "inset 0px -1px 0px rgba(255, 255, 255, 0.18)",
                                }}
                                className='w-full rounded-[0.5rem] bg-richblack-800 p-[12px] text-richblack-5'
                            />
                            <span
                            onClick={() => setShowPassword((prev) => !prev)}
                            className="absolute right-3 top-[38px] z-[10] cursor-pointer"
                            >
                            {showPassword ? (
                                <FaEyeSlash fontSize={24} fill="#AFB2BF" />
                            ) : (
                                <FaEye fontSize={24} fill="#AFB2BF" />
                            )}
                            </span>
                        </label>

                        <input 
                            type='file'
                            accept='.csv'
                            onChange={handleFileUpload}
                            className='text-richblack-5'
                        />

                        <button
                            type='submit'
                            className='bg-[#e0e1dd] py-1 rounded-sm'
                        >
                            Login
                        </button>
                        
                    </form>
        </div>
        
    </div>
  )
}

export default Login