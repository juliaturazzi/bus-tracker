import { fetchData } from '../api/Api';

global.fetch = jest.fn(() =>
  Promise.resolve({
    ok: true,
    json: () => Promise.resolve({ data: 'sample data' }),
  })
);

describe('fetchData', () => {
  afterEach(() => {
    jest.clearAllMocks();
  });

  it('fetches data successfully', async () => {
    const formData = {
      bus_line: '123',
      bus_stop: 'Main St',
      start_time: '08:00',
      end_time: '09:00',
      email: 'test@example.com',
    };

    const data = await fetchData(formData);

    expect(global.fetch).toHaveBeenCalledTimes(1);
    expect(global.fetch).toHaveBeenCalledWith(
      `http://localhost:8000/infos/?bus_line=123&start_time=08:00&end_time=09:00&bus_stop=Main%20St&email=test@example.com`
    );
    expect(data).toEqual({ data: 'sample data' });
  });

  it('throws an error when response is not ok', async () => {
    global.fetch.mockImplementationOnce(() =>
      Promise.resolve({
        ok: false,
      })
    );

    const formData = {
      bus_line: '123',
      bus_stop: 'Main St',
      start_time: '08:00',
      end_time: '09:00',
      email: 'test@example.com',
    };

    await expect(fetchData(formData)).rejects.toThrow('Error in response');
  });

  it('throws an error when fetch fails', async () => {
    global.fetch.mockImplementationOnce(() =>
      Promise.reject(new Error('Fetch failed'))
    );

    const formData = {
      bus_line: '123',
      bus_stop: 'Main St',
      start_time: '08:00',
      end_time: '09:00',
      email: 'test@example.com',
    };

    await expect(fetchData(formData)).rejects.toThrow('Fetch failed');
  });
});
