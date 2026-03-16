import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'

describe('LoadingSpinner', () => {
  it('renders properly', () => {
    const wrapper = mount(LoadingSpinner)
    expect(wrapper.exists()).toBe(true)
  })

  it('displays loading text when provided', () => {
    const text = 'Loading data...'
    const wrapper = mount(LoadingSpinner, {
      props: { text },
    })
    expect(wrapper.text()).toContain(text)
  })

  it('has correct CSS classes', () => {
    const wrapper = mount(LoadingSpinner)
    expect(wrapper.classes()).toContain('flex')
    expect(wrapper.classes()).toContain('items-center')
  })

  it('renders spinner element', () => {
    const wrapper = mount(LoadingSpinner)
    const spinner = wrapper.find('.animate-spin')
    expect(spinner.exists()).toBe(true)
  })
})
