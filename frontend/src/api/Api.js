export const fetchData = async (formData) => {
  try {
    const bus_line = formData.bus_line;
    const bus_stop = formData.bus_stop;
    const start_time = formData.start_time;
    const end_time = formData.end_time;
    const email = formData.email;
    
    const request_variables = `bus_line=${bus_line}&start_time=${start_time}&end_time=${end_time}&bus_stop=${bus_stop}&email=${email}`
    const response = await fetch(`http://localhost:8000/infos/?${request_variables}`);
    
    if (!response.ok) {
      throw new Error("Error in response");
    }
    return await response.json();
  } catch (error) {
    throw error;
  }
};
